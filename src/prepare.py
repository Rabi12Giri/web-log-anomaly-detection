# prepare.py
# This script parses the raw Apache access.log file
# and converts it into a structured CSV file

import re
import csv
from tqdm import tqdm
from datetime import datetime
from pathlib import Path

# Default paths
DEFAULT_LOG_FILE = "data/raw/access.log"
DEFAULT_OUTPUT_FILE = "data/processed/parsed_logs.csv"

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

    # Convert timestamp to datetime
    data["time"] = datetime.strptime(
        data["time"].split()[0],
        "%d/%b/%Y:%H:%M:%S"
    )

    return data


def parse_logs(
    log_file: str = DEFAULT_LOG_FILE,
    output_file: str = DEFAULT_OUTPUT_FILE,
    show_progress: bool = True
):
    """
    Parses an Apache log file and writes parsed rows to CSV.

    This function is SAFE for:
    - manual execution
    - automated background jobs
    - live log files (append-based)

    Parameters:
    - log_file: path to raw .log file
    - output_file: path to output CSV
    - show_progress: disable tqdm in automation
    """

    log_path = Path(log_file)
    if not log_path.exists():
        print(f"[prepare] Log file not found: {log_file}")
        return

    with open(log_path, "r", encoding="utf-8", errors="ignore") as infile, \
         open(output_file, "w", newline="", encoding="utf-8") as outfile:

        fieldnames = ["ip", "time", "method", "url", "status", "agent"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        iterator = infile
        if show_progress:
            iterator = tqdm(infile, desc="Processing log lines")

        for line in iterator:
            parsed = parse_log_line(line)
            if parsed:
                writer.writerow(parsed)


def main():
    print("Starting log parsing (manual mode)...")
    parse_logs()
    print("Parsing completed. Output saved to parsed_logs.csv")


if __name__ == "__main__":
    main()
