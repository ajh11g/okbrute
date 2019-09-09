# okbrute.py

## Description
Simple python script to test credentials against an Okta hosted Sign-In widget. Just supply the subdomain (`<target>.okta.com`), username(s), and password(s) and it'll take care of the rest. Only uses the Python standard library.


## Options

```
usage: okbrute.py [-h] [--target TARGET] [-u USER] [-p PASSWORD]      
                    [--userlist USERLIST] [--passwordlist PASSWORDLIST] 
                    [--limit LIMIT]

For testing username/password combos against an Okta sign-in widget.

optional arguments:
  -h, --help            show this help message and exit
  --target TARGET       The target subdomain (https://<target>.okta.com)
  -u USER, --user USER  Single username to try
  -p PASSWORD, --password PASSWORD
                        Single password to try
  --userlist USERLIST   A file containing the list of usernames
  --passwordlist PASSWORDLIST
                        A file containig the list of passwords
  --limit LIMIT         Set request rate limit speed, in seconds   
```

## Example Output
Testing a single user against multiple passwords:
```
python okbrute.py --target <target> -u bob --passwordlist passwords --limit 3
[-] Testing 1 username(s) and 2 password(s) against <target>.okta.com
[!] Authentication failure for bob:test
[!] Authentication failure for bob:password
```

Testing multiple users and multiple passwords:
```
python okbrute_final.py --target <target> --userlist users --passwordlist passwords --limit 3
[-] Testing 2 username(s) and 2 password(s) against <target>.okta.com
[!] Authentication failure for test:test
[!] Authentication failure for bob:test
[!] Authentication failure for test:password
[!] Authentication failure for bob:password
```
