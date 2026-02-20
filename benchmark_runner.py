"""Run reproducible benchmarks on 3+ open-source repositories.

Usage:
    python benchmark_runner.py
"""

from time import perf_counter
import json

from compressor import compress, count_tokens
from rag import CodeRAG
from repo_loader import load_repo


DEFAULT_REPOS = [
    "https://github.com/pallets/flask",
    "https://github.com/psf/requests",
    "https://github.com/streamlit/streamlit",
]

SAMPLE_QUERIES = [
    "Where is authentication handled?",
    "Which files define API endpoints?",
    "How is configuration loaded?",
]


def benchmark_repo(repo_url):
    start = perf_counter()
    chunks, _ = load_repo(repo_url)
    load_seconds = perf_counter() - start

    processed = []
    for c in chunks:
        compressed = compress(
            c["code"],
            imports=c.get("imports"),
            dependencies=c.get("dependencies"),
            surrounding=c.get("surrounding"),
        )
        processed.append(
            {
                "path": c["path"],
                "symbol": c.get("symbol", "module"),
                "chunk_type": c.get("chunk_type", "module"),
                "dependencies": c.get("dependencies", []),
                "language": c.get("language", "unknown"),
                "original_tokens": count_tokens(c["code"]),
                "compressed_tokens": count_tokens(compressed),
                "compressed": compressed,
            }
        )

    rag = CodeRAG()
    rag.add(processed)

    q_times = []
    for q in SAMPLE_QUERIES:
        q_start = perf_counter()
        rag.query(q)
        q_times.append(perf_counter() - q_start)

    original = sum(x["original_tokens"] for x in processed) if processed else 0
    compressed = sum(x["compressed_tokens"] for x in processed) if processed else 0
    ratio = (1 - (compressed / original)) * 100 if original else 0
    return {
        "repo": repo_url,
        "chunks": len(processed),
        "load_seconds": round(load_seconds, 2),
        "avg_query_seconds": round(sum(q_times) / len(q_times), 3) if q_times else 0.0,
        "original_tokens": original,
        "compressed_tokens": compressed,
        "compression_percent": round(ratio, 2),
    }


def main():
    rows = [benchmark_repo(url) for url in DEFAULT_REPOS]
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
