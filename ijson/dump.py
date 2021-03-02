'''Dumping command-line utility'''

import argparse
import sys

import ijson
from . import compat


HEADERS = {
    'basic_parse': 'name, value',
    'parse': 'path, name, value',
    'kvitems': 'key, value',
    'items': 'value',
}

def to_string(o):
    if isinstance(o, compat.texttype) and compat.IS_PY2:
        o = o.encode('utf8')
    if isinstance(o, compat.bytetype):
        return compat.b2s(o)
    return str(o)

def dump():
    parser = argparse.ArgumentParser(description='Dump ijson events')
    parser.add_argument('-m', '--method', choices=['basic_parse', 'parse', 'kvitems', 'items'],
                        help='The method to use for dumping', default='basic_parse')
    parser.add_argument('-p', '--prefix', help='Prefix (used with -M items|kvitems)', default='')
    args = parser.parse_args()

    method = getattr(ijson, args.method)
    method_args = ()
    if args.method in ('items', 'kvitems'):
        method_args = args.prefix,
    header = '#: ' + HEADERS[args.method]
    print(header)
    print('-' * len(header))

    # Use the raw bytes stream in stdin if possible
    stdin = sys.stdin
    if hasattr(stdin, 'buffer'):
        stdin = stdin.buffer

    enumerated_results = enumerate(method(stdin, *method_args))
    if args.method == 'items':
        for i, result in enumerated_results:
            print('%i: %s' % (i, result))
    else:
        for i, result in enumerated_results:
            print('%i: %s' % (i, ', '.join(to_string(bit) for bit in result)))

if __name__ == '__main__':
    dump()