#!/usr/bin/python3

# INET4031 - Enhanced User Creation with Interactive Dry-Run
# Feyzan Ali
# Date Created: November 05, 2025
# Date Last Modified: November 07, 2025

import os
import re
import sys

def main():
    # === CHECK FOR INPUT FILE ARGUMENT ===
    if len(sys.argv) != 2:
        print("Usage: sudo ./create-users2.py <input-file>")
        print("Example: sudo ./create-users2.py create-users.input")
        sys.exit(1)

    input_file = sys.argv[1]

    # === INTERACTIVE DRY-RUN PROMPT (from real terminal) ===
    print("Run in dry-run mode? (Y/N): ", end='', flush=True)
    response = input().strip().upper()
    dry_run = response == 'Y'

    if dry_run:
        print("\nDRY RUN MODE: No changes will be made.\n")
    else:
        print("\nREAL RUN MODE: Users will be created.\n")

    # === READ INPUT FILE LINE BY LINE ===
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Skip comments
        if re.match(r"^#", line):
            if dry_run:
                print(f"[DRY] Skipping: {line}")
            continue

        fields = line.split(':')
        if len(fields) != 5:
            if dry_run:
                print(f"[DRY] ERROR: Bad format: {line}")
            continue

        username = fields[0]
        password = fields[1]
        gecos = f"{fields[3]} {fields[2]},,,"
        group_list = [g.strip() for g in fields[4].split(',') if g.strip() and g.strip() != '-']

        # === CREATE USER ===
        cmd = f"adduser --disabled-password --gecos '{gecos}' {username}"
        if dry_run:
            print(f"[DRY] {cmd}")
        else:
            print(f"==> Creating {username}...")
            result = os.system(cmd)
            if result != 0:
                print(f"Failed to create {username}")
                continue

        # === SET PASSWORD ===
        cmd = f"echo '{password}\n{password}' | passwd {username}"
        if dry_run:
            print(f"[DRY] {cmd}")
        else:
            print(f"==> Setting password for {username}...")
            os.system(cmd)

        # === ADD TO GROUPS ===
        for group in group_list:
            cmd = f"adduser {username} {group}"
            if dry_run:
                print(f"[DRY] {cmd}")
            else:
                print(f"==> Adding {username} to {group}...")
                os.system(cmd)

    print("\nOperation complete.")

if __name__ == '__main__':
    main()