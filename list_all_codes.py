#!/usr/bin/env python

from __future__ import print_function
import lsi_decode_loginfo as loginfo

def generate_values(data):
    title = data[0]
    mask = data[1]
    sub = data[2]

    for key in sub.keys():
        v = sub[key]
        key_name = v[0]
        key_sub = v[1]
        key_detail = v[2]
        if key_sub is None:
            yield [(title, key, key_name, key_detail)]
        else:
            for sub_val in generate_values(key_sub):
                yield [(title, key, key_name, key_detail)] + sub_val

for entry in generate_values(loginfo.types):
    val = 0
    for line in entry:
        val |= line[1]
    print('    %-10s\t0x%08X' % ('Value', val))
    for line in entry:
        print('    %-10s\t0x%08X %s %s' % (line[0], line[1], line[2], line[3]))
    print()
    print('&nbsp;')
    print()
