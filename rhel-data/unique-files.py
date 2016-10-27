#!/usr/bin/python

import sys

def main(sumfile):
    sums = [line.strip().split(None,1) for line in open(sumfile)]
    uniq_sums = dict(sums)
    for shasum, filename in uniq_sums.items():
        print("{}  {}".format(shasum,filename))

if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except IOError as e:
        print(str(e))
        raise SystemExit(1)
    except KeyboardInterrupt:
        raise SystemExit(2)
