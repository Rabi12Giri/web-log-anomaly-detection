import re
import csv

# ===== CONFIG =====
LOG_FILE = "data/raw/access.log"          
OUTPUT_CSV = "temp/access_preview.csv"
MAX_ROWS = 50000                 # rows to export
# ==================

# Regex for common access.log format
log_pattern = re.compile(
    r'(?P<ip>\S+) '              # IP address
    r'\S+ \S+ '                  # identity, user (ignored)
    r'\[(?P<time>[^\]]+)\] '     # timestamp
    r'"(?P<method>\S+) '         # HTTP method
    r'(?P<url>\S+) '             # URL
    r'(?P<protocol>[^"]+)" '     # protocol
    r'(?P<status>\d+) '          # status code
    r'(?P<size>\S+)'             # response size
)

with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as log, \
     open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:

    writer = csv.writer(csvfile)
    
    # CSV Header
    writer.writerow([
        "ip",
        "timestamp",
        "method",
        "url",
        "protocol",
        "status",
        "response_size"
    ])

    row_count = 0

    for line in log:
        match = log_pattern.search(line)
        if match:
            writer.writerow([
                match.group("ip"),
                match.group("time"),
                match.group("method"),
                match.group("url"),
                match.group("protocol"),
                match.group("status"),
                match.group("size")
            ])
            row_count += 1

        if row_count >= MAX_ROWS:
            break

print(f"Done! {row_count} rows written to {OUTPUT_CSV}")
