# INET4031 Add Users Script and User List

## Program Description

This Python script automates the creation of multiple Linux user accounts and their group memberships using data from a structured input file (`create-users.input`). It eliminates the need to manually run `adduser`, `passwd`, and group assignment commands for each user.

Normally, an admin would:
```bash
sudo adduser --gecos "First Last,,," username
echo 'pass\npass' | sudo passwd username
sudo adduser username groupname
```

This script reads colon-delimited user data, parses it, and executes the equivalent `adduser` and `passwd` commands programmatically, ensuring consistency and reducing errors across multiple servers.

## Program User Operation

### Input File Format

File: `create-users.input`
Each line represents one user with 5 colon-separated fields:
```bash
username:password:lastname:firstname:groups
```

* groups: comma-separated list (e.g., group01,group02)
* Use - to assign no groups
* Use # at start of line to skip (comment out)
* Malformed lines (wrong field count) are silently skipped

**Example**

```bash
user04:pass04:Last04:First04:group01
user07:pass07:Last07:First07:-
#user08:pass08:Last08:First08:group01
```

## Command Execution

1.  Make script executable:

```bash
    chmod +x create-users.py
 ```

2.  Run with sudo (required for user management):

```bash
    sudo ./create-users.py < create-users.input
```

## Dry Run

Not supported in this version. Use create-users2.py for interactive dry-run mode (see repo contents).

See create-users2.py for enhanced version with dry-run support.


```bash
$ git add README.md
$ git commit -m "Add professional README.md"
$ git push origin main
```