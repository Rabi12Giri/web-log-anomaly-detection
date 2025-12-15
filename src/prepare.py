# prepare.py
# This script parses the raw Apache access.log file
# and converts it into a structured CSV file

import re
import csv
from tqdm import tqdm
from datetime import datetime

# Path to raw log file
LOG_FILE = "data/raw/access.log"

# Output CSV file
OUTPUT_FILE = "data/processed/parsed_logs.csv"

# Apache combined log format regex
LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) \S+ \S+ '
    r'\[(?P<time>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<url>\S+) \S+" '
    r'(?P<status>\d{3}) \S+ '
    r'"[^"]*" "(?P<agent>[^"]*)"'
)

def parse_log_line(line):
    """
    Parses a single log line and extracts fields.
    Returns a dictionary or None if parsing fails.
    """
    match = LOG_PATTERN.search(line)
    if not match:
        return None

    data = match.groupdict()

    # Convert timestamp to readable format
    data["time"] = datetime.strptime(
        data["time"].split()[0],
        "%d/%b/%Y:%H:%M:%S"
    )

    return data


def main():
    print("Starting log parsing...")

    with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as infile, \
         open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as outfile:

        fieldnames = ["ip", "time", "method", "url", "status", "agent"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for line in tqdm(infile, desc="Processing log lines"):
            parsed = parse_log_line(line)
            if parsed:
                writer.writerow(parsed)

    print("Parsing completed. Output saved to parsed_logs.csv")


if __name__ == "__main__":
    main()
