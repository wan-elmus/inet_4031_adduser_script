#!/usr/bin/python3

# INET4031 - Enhanced User Creation with Dry-Run Mode
# Feyzan Ali
# Date Created: November 05, 2025
# Date Last Modified: November 07, 2025

import os
import re
import sys

def main():
    # Interactive dry-run prompt
    response = input("Run in dry-run mode? (Y/N): ").strip().upper()
    dry_run = response == 'Y'

    if dry_run:
        print("DRY RUN MODE: No changes will be made to the system.\n")

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        # Skip commented lines
        if re.match("^#", line):
            if dry_run:
                print(f"Skipping commented line: {line}")
            continue

        fields = line.split(':')
        if len(fields) != 5:
            if dry_run:
                print(f"ERROR: Malformed line (expected 5 fields): {line}")
            continue

        username = fields[0]
        password = fields[1]
        gecos = f"{fields[3]} {fields[2]},,,"
        group_list = fields[4].split(',')

        # User creation
        cmd = f"/usr/sbin/adduser --disabled-password --gecos '{gecos}' {username}"
        if dry_run:
            print(f"[DRY] Would run: {cmd}")
        else:
            print(f"==> Creating account for {username}...")
            os.system(cmd)

        # Password setting
        cmd = f"/bin/echo -ne '{password}\n{password}' | /usr/bin/sudo /usr/bin/passwd {username}"
        if dry_run:
            print(f"[DRY] Would run: {cmd}")
        else:
            print(f"==> Setting password for {username}...")
            os.system(cmd)

        # Group assignment
        for group in group_list:
            if group != '-' and group.strip():
                cmd = f"/usr/sbin/adduser {username} {group}"
                if dry_run:
                    print(f"[DRY] Would run: {cmd}")
                else:
                    print(f"==> Assigning {username} to {group}...")
                    os.system(cmd)

    if dry_run:
        print("\nDry run complete. No users were added.")

if __name__ == '__main__':
    main()