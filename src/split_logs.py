# split_logs.py
# One-time utility script to split access.log into small chunks
# Used for simulated live log ingestion

from pathlib import Path

SOURCE_LOG = Path("data/raw/access.log")
CHUNK_DIR = Path("data/raw/chunks")
LINES_PER_CHUNK = 50 

def split_logs():
    if not SOURCE_LOG.exists():
        print("[split_logs] Source log file not found.")
        return

    CHUNK_DIR.mkdir(parents=True, exist_ok=True)

    with open(SOURCE_LOG, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    if not lines:
        print("[split_logs] Source log is empty.")
        return

    chunk_count = 0

    for i in range(0, len(lines), LINES_PER_CHUNK):
        chunk_lines = lines[i:i + LINES_PER_CHUNK]
        chunk_file = CHUNK_DIR / f"log_{chunk_count}.log"

        with open(chunk_file, "w", encoding="utf-8") as out:
            out.writelines(chunk_lines)

        chunk_count += 1

    print(f"[split_logs] Created {chunk_count} log chunks successfully.")
    print(f"[split_logs] Location: {CHUNK_DIR}")

if __name__ == "__main__":
    split_logs()
