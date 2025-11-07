#!/usr/bin/python3

# INET4031 - Automated User Creation Script
# Feyzan Ali
# Date Created: November 05, 2025
# Date Last Modified: November 07, 2025

# os: Execute system commands (adduser, passwd)
# re: Match comment lines starting with '#'
# sys: Read input data from stdin (piped from input file)
import os
import re
import sys

def main():
    # Process each line from the input file (via stdin)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        # Detect and skip commented lines (start with '#')
        if re.match("^#", line):
            continue

        # Split line into exactly 5 colon-separated fields
        fields = line.split(':')
        if len(fields) != 5:
            continue  # Skip malformed lines

        # Extract user information
        username = fields[0]
        password = fields[1]
        gecos = f"{fields[3]} {fields[2]},,,"  # GECOS: First Last,,,

        # Parse group memberships (comma-separated; '-' = no groups)
        group_list = fields[4].split(',')

        # Create user account with GECOS and no password prompt
        print(f"==> Creating account for {username}...")
        cmd = f"/usr/sbin/adduser --disabled-password --gecos '{gecos}' {username}"
        os.system(cmd)

        # Set user password using echo + passwd
        print(f"==> Setting the password for {username}...")
        cmd = f"/bin/echo -ne '{password}\n{password}' | /usr/bin/sudo /usr/bin/passwd {username}"
        os.system(cmd)

        # Add user to specified groups (skip if '-')
        for group in group_list:
            if group != '-' and group.strip():
                print(f"==> Assigning {username} to the {group} group...")
                cmd = f"/usr/sbin/adduser {username} {group}"
                os.system(cmd)

if __name__ == '__main__':
    main()