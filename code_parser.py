"""Tree-sitter based code chunk extraction.

Extracts module/class/function level chunks with imports and lightweight
dependency hints so retrieval can work on structural code units.
"""

import ast
from functools import lru_cache
import re

try:
    from tree_sitter_languages import get_parser
    HAS_TREE_SITTER = True
except Exception:
    get_parser = None
    HAS_TREE_SITTER = False


EXT_TO_LANGUAGE = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".java": "java",
    ".c": "c",
    ".h": "c",
    ".cpp": "cpp",
}

SYMBOL_NODE_TYPES = {
    "python": {"function_definition": "function", "class_definition": "class"},
    "javascript": {"function_declaration": "function", "class_declaration": "class", "method_definition": "method"},
    "typescript": {"function_declaration": "function", "class_declaration": "class", "method_definition": "method"},
    "java": {"method_declaration": "function", "class_declaration": "class", "interface_declaration": "class"},
    "c": {"function_definition": "function", "struct_specifier": "class"},
    "cpp": {"function_definition": "function", "class_specifier": "class", "struct_specifier": "class"},
}

IMPORT_NODE_TYPES = {
    "python": {"import_statement", "import_from_statement"},
    "javascript": {"import_statement"},
    "typescript": {"import_statement"},
    "java": {"import_declaration"},
    "c": {"preproc_include"},
    "cpp": {"preproc_include"},
}


@lru_cache(maxsize=16)
def _get_parser(language):
    if not HAS_TREE_SITTER:
        return None
    return get_parser(language)


def _file_language(path):
    dot = path.rfind(".")
    if dot == -1:
        return None
    return EXT_TO_LANGUAGE.get(path[dot:].lower())


def _walk(node):
    stack = [node]
    while stack:
        cur = stack.pop()
        yield cur
        for child in reversed(cur.children):
            stack.append(child)


def _node_text(source_bytes, node):
    return source_bytes[node.start_byte:node.end_byte].decode("utf-8", errors="ignore")


def _extract_symbol_name(source_bytes, node):
    name_node = node.child_by_field_name("name")
    if name_node is not None:
        return _node_text(source_bytes, name_node).strip()
    header = _node_text(source_bytes, node).splitlines()[0].strip()
    if not header:
        return "anonymous"
    return header[:80]


def _extract_dependencies(chunk_code, symbols, self_symbol):
    tokens = re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", chunk_code)
    seen = set()
    deps = []
    for t in tokens:
        if t == self_symbol or t not in symbols or t in seen:
            continue
        seen.add(t)
        deps.append(t)
        if len(deps) >= 12:
            break
    return deps


def parse_code_chunks(path, code):
    """Return structural chunks for a source file using tree-sitter.

    Returns list of dictionaries:
        path, symbol, chunk_type, code, imports, dependencies, surrounding, language
    """
    language = _file_language(path)
    if not language:
        return []

    parser = _get_parser(language)
    if parser is None:
        return _fallback_parse_chunks(path, code, language)

    source_bytes = code.encode("utf-8", errors="ignore")
    try:
        tree = parser.parse(source_bytes)
    except Exception:
        return _fallback_parse_chunks(path, code, language)
    root = tree.root_node

    import_nodes = []
    symbol_nodes = []
    symbol_type_map = SYMBOL_NODE_TYPES.get(language, {})
    import_types = IMPORT_NODE_TYPES.get(language, set())

    for node in _walk(root):
        if node.type in import_types:
            import_nodes.append(node)
        if node.type in symbol_type_map:
            symbol_nodes.append(node)

    imports = [_node_text(source_bytes, n).strip() for n in import_nodes][:25]
    symbol_nodes.sort(key=lambda n: n.start_byte)
    symbol_names = [_extract_symbol_name(source_bytes, n) for n in symbol_nodes]
    symbol_set = set(symbol_names)

    chunks = []
    module_summary = "\n".join(code.splitlines()[:80])
    chunks.append(
        {
            "path": path,
            "symbol": "module",
            "chunk_type": "module",
            "code": module_summary if module_summary.strip() else code[:3000],
            "imports": imports,
            "dependencies": symbol_names[:15],
            "surrounding": [],
            "language": language,
        }
    )

    for idx, node in enumerate(symbol_nodes):
        symbol_name = symbol_names[idx]
        chunk_code = _node_text(source_bytes, node)
        previous_symbol = symbol_names[idx - 1] if idx > 0 else None
        next_symbol = symbol_names[idx + 1] if idx + 1 < len(symbol_names) else None
        surrounding = [s for s in [previous_symbol, next_symbol] if s]
        dependencies = _extract_dependencies(chunk_code, symbol_set, symbol_name)

        chunks.append(
            {
                "path": path,
                "symbol": symbol_name,
                "chunk_type": symbol_type_map.get(node.type, "symbol"),
                "code": chunk_code,
                "imports": imports,
                "dependencies": dependencies,
                "surrounding": surrounding,
                "language": language,
            }
        )

    if not chunks:
        return _fallback_parse_chunks(path, code, language)
    return chunks


def _extract_import_lines(language, code):
    lines = code.splitlines()
    imports = []
    if language == "python":
        for ln in lines:
            s = ln.strip()
            if s.startswith("import ") or s.startswith("from "):
                imports.append(s)
    elif language in {"javascript", "typescript"}:
        for ln in lines:
            s = ln.strip()
            if s.startswith("import ") or s.startswith("const ") and "require(" in s:
                imports.append(s)
    elif language == "java":
        for ln in lines:
            s = ln.strip()
            if s.startswith("import "):
                imports.append(s)
    elif language in {"c", "cpp"}:
        for ln in lines:
            s = ln.strip()
            if s.startswith("#include"):
                imports.append(s)
    return imports[:25]


def _extract_python_symbol_blocks(code):
    chunks = []
    try:
        tree = ast.parse(code)
    except Exception:
        return chunks

    lines = code.splitlines()
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        start = max(1, getattr(node, "lineno", 1))
        end = getattr(node, "end_lineno", start)
        code_block = "\n".join(lines[start - 1:end]).strip()
        chunk_type = "class" if isinstance(node, ast.ClassDef) else "function"
        symbol = getattr(node, "name", "anonymous")
        chunks.append((symbol, chunk_type, code_block))
    return chunks


def _extract_regex_symbols(language, code):
    patterns = []
    if language in {"javascript", "typescript"}:
        patterns = [
            (re.compile(r"^\s*class\s+([A-Za-z_][A-Za-z0-9_]*)"), "class"),
            (re.compile(r"^\s*function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\("), "function"),
            (re.compile(r"^\s*const\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\("), "function"),
        ]
    elif language == "java":
        patterns = [
            (re.compile(r"^\s*(public|private|protected)?\s*class\s+([A-Za-z_][A-Za-z0-9_]*)"), "class"),
            (re.compile(r"^\s*(public|private|protected)?\s*[\w<>\[\]]+\s+([A-Za-z_][A-Za-z0-9_]*)\s*\("), "function"),
        ]
    elif language in {"c", "cpp"}:
        patterns = [
            (re.compile(r"^\s*(class|struct)\s+([A-Za-z_][A-Za-z0-9_]*)"), "class"),
            (re.compile(r"^\s*[\w\*\s]+\s+([A-Za-z_][A-Za-z0-9_]*)\s*\([^;]*\)\s*\{"), "function"),
        ]

    chunks = []
    lines = code.splitlines()
    for idx, ln in enumerate(lines):
        for pat, typ in patterns:
            m = pat.match(ln)
            if not m:
                continue
            symbol = m.group(m.lastindex) if m.lastindex else "anonymous"
            start = max(0, idx - 2)
            end = min(len(lines), idx + 18)
            block = "\n".join(lines[start:end]).strip()
            if block:
                chunks.append((symbol, typ, block))
            break
    return chunks


def _fallback_parse_chunks(path, code, language):
    imports = _extract_import_lines(language, code)
    lines = code.splitlines()
    module_summary = "\n".join(lines[:80]) if lines else code[:3000]
    raw_symbols = []

    if language == "python":
        raw_symbols = _extract_python_symbol_blocks(code)
    if not raw_symbols:
        raw_symbols = _extract_regex_symbols(language, code)

    symbol_names = [s[0] for s in raw_symbols]
    symbol_set = set(symbol_names)
    chunks = [
        {
            "path": path,
            "symbol": "module",
            "chunk_type": "module",
            "code": module_summary,
            "imports": imports,
            "dependencies": symbol_names[:15],
            "surrounding": [],
            "language": language,
        }
    ]

    for idx, (symbol, chunk_type, chunk_code) in enumerate(raw_symbols):
        previous_symbol = symbol_names[idx - 1] if idx > 0 else None
        next_symbol = symbol_names[idx + 1] if idx + 1 < len(symbol_names) else None
        surrounding = [s for s in [previous_symbol, next_symbol] if s]
        dependencies = _extract_dependencies(chunk_code, symbol_set, symbol)
        chunks.append(
            {
                "path": path,
                "symbol": symbol,
                "chunk_type": chunk_type,
                "code": chunk_code,
                "imports": imports,
                "dependencies": dependencies,
                "surrounding": surrounding,
                "language": language,
            }
        )
    return chunks
