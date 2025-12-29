import pandas as pd

df = pd.read_csv(
    "data/raw/access.log",
    nrows=5
)

print(df.head(10))

# import re

# LOG_FILE = "data/raw/access.log"
# MAX_PRINT = 10

# # Same regex used for CSV generation
# log_pattern = re.compile(
#     r'(?P<ip>\S+) '
#     r'\S+ \S+ '
#     r'\[(?P<time>[^\]]+)\] '
#     r'"(?P<method>\S+) '
#     r'(?P<url>\S+) '
#     r'(?P<protocol>[^"]+)" '
#     r'(?P<status>\d+) '
#     r'(?P<size>\S+)'
# )

# print("ip | timestamp | method | url | protocol | status | response_size")
# print("-" * 90)

# printed = 0

# with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as file:
#     for line in file:
#         match = log_pattern.search(line)
#         if match:
#             print(
#                 f"{match.group('ip')} | "
#                 f"{match.group('time')} | "
#                 f"{match.group('method')} | "
#                 f"{match.group('url')} | "
#                 f"{match.group('protocol')} | "
#                 f"{match.group('status')} | "
#                 f"{match.group('size')}"
#             )
#             printed += 1

#         if printed >= MAX_PRINT:
#             break

# print(f"\nPrinted {printed} rows from access.log")
