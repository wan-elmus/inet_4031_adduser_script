#!/usr/bin/python3

# INET4031
# Feyzan Ali
# Date Created: November 05, 2025
# Date Last Modified: November 07, 2025

# os: to execute system commands (adduser, passwd)
# re: for regular expression matching (to detect comment lines)
# sys: to read input from stdin (piped input file)
import os
import re
import sys

def main():
    for line in sys.stdin:

        # Check if line starts with '#' → used to comment out/skip a user
        match = re.match("^#", line)

        # Split line into fields using ':' as delimiter
        fields = line.strip().split(':')

        # Skip lines that are comments OR do not have exactly 5 fields
        # This prevents malformed input from crashing the script
        if match or len(fields) != 5:
            continue

        # Map input fields to user account data
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3], fields[2])  # Format: First Last,,,

        # Parse groups field (comma-separated); '-' means no groups
        groups = fields[4].split(',')

        print("==> Creating account for %s..." % (username))
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos, username)
        print(cmd)  # Dry-run: show command
        os.system(cmd)  # Real run: execute

        print("==> Setting the password for %s..." % (username))
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password, password, username)
        print(cmd)
        os.system(cmd)

        for group in groups:
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username, group))
                cmd = "/usr/sbin/adduser %s %s" % (username, group)
                print(cmd)
                os.system(cmd)

if __name__ == '__main__':
    main()