#!/usr/bin/env python3
"""
process_imessage_numbers.py

Reads a CSV of phone numbers (one per line) from the current directory,
checks which are iMessage-enabled using the same logic as the original script,
and writes out a CSV containing only the iMessage-enabled numbers.

Usage:
    python process_imessage_numbers.py input_numbers.csv --output imessage_only.csv

Configuration:
- Place your server URL in credentials.txt (first line).
- Place your API password in pwd.txt (first line).
"""

import os
import sys
import argparse
import urllib.request
import urllib.parse
import json
import re
import time
import random

# ─── CONFIG ───────────────────────────────────────────────────────────────────
BASE = os.getcwd()

# Read SERVER_URL from credentials.txt in current directory
def read_first_line(filename):
    try:
        with open(os.path.join(BASE, filename), 'r') as f:
            line = f.readline().strip()
            if not line:
                raise ValueError(f"Empty {filename}")
            return line
    except Exception as e:
        print(f"[CONFIG ERROR] reading {filename}: {e}", file=sys.stderr)
        sys.exit(1)

SERVER_URL = read_first_line('credentials.txt')
API_PASSWORD = read_first_line('pwd.txt')
# ─── END CONFIG ───────────────────────────────────────────────────────────────

def normalize_us_number(raw):
    digits = re.sub(r'\D', '', raw or "")
    if len(digits) == 10:
        return "+1" + digits
    if len(digits) == 11 and digits.startswith("1"):
        return "+" + digits
    return "+" + digits


def classify_numbers(numbers):
    """
    Checks iMessage availability for a list of normalized numbers.
    Returns (status_dict, errored_list).
    status_dict maps number -> True/False (iMessage enabled).
    errored_list contains numbers that failed to check.
    """
    status = {}
    errored = []
    for num in numbers:
        delay = random.uniform(5, 10)
        print(f"Waiting {delay:.1f}s before checking {num}", file=sys.stderr)
        time.sleep(delay)

        addr = urllib.parse.quote(num)
        url = (
            f"{SERVER_URL}/api/v1/handle/availability/imessage"
            f"?password={API_PASSWORD}&address={addr}"
        )
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'application/json',
                'Connection': 'close'
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode('utf-8'))
            ok = (data.get('status') == 200 and data.get('data', {}).get('available', False))
            status[num] = bool(ok)
        except Exception as e:
            print(f"Error checking {num}: {e}", file=sys.stderr)
            errored.append(num)
    return status, errored


def main():
    parser = argparse.ArgumentParser(
        description="Check iMessage availability for a list of phone numbers."
    )
    parser.add_argument(
        "input_csv", help="CSV file (one phone number per line) in current directory"
    )
    parser.add_argument(
        "--output", "-o",
        default="imessage_numbers.csv",
        help="Output CSV for iMessage-enabled numbers"
    )
    args = parser.parse_args()

    # Read raw numbers
    try:
        with open(args.input_csv, 'r') as f:
            raw_numbers = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)

    # Normalize and dedupe
    normalized = [normalize_us_number(n) for n in raw_numbers]
    unique_numbers = sorted(set(normalized))
    print(f"Checking {len(unique_numbers)} unique phone numbers...")

    # Check availability
    results, errored_nums = classify_numbers(unique_numbers)

    # Filter only iMessage-enabled
    imessage_only = [num for num, ok in results.items() if ok]

    # Write output
    try:
        with open(args.output, 'w') as f:
            for num in imessage_only:
                f.write(num + "\n")
        print(f"Wrote iMessage-enabled numbers to {args.output}")
    except Exception as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
