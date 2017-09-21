#!/usr/bin/env python
"""
Check the accuracy of an Irish Personal Public Service (PPS) number.
https://en.wikipedia.org/wiki/Personal_Public_Service_Number

"""
import re
import sys

CHECK_CHARS = 'WABCDEFGHIJKLMNOPQRSTUV'


class PpsException(Exception):
    pass


def check_pps(pps='1234567T'):
    pps = pps.strip().upper()
    if not re.match('^[0-9]{7}[A-Z]W?$', pps):
        raise PpsException('not in the form 1234567A')

    digits = (int(d) for d in pps[:7])
    wsum = sum(d * (8 - i) for (i, d) in enumerate(digits))
    checksum = CHECK_CHARS[wsum % 23]
    if pps[7] != checksum:
        raise PpsException('check character does not match')
    return True


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('pps_no')

    if not sys.argv:
        parser.print_help()
        return 1

    args = parser.parse_args()

    try:
        check_pps(args.pps_no)
    except PpsException as err:
        sys.stderr.write('invalid: %s\n' % err)
        return 1
    print('PPS number is valid')

if __name__ == '__main__':
    sys.exit(main())
