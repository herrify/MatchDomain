#!/usr/bin/env python3
#
# @author: johnny
# created: 2016-12-23
# description
#   replace
#     sshpass -p {PASS} ssh -o StrictHostKeyChecking=no -C -D 0.0.0.0:{LOCAL_PORT} -p 31222 root@seaof-153-125-231-179.jp-tokyo-02.arukascloud.io
#   or 
#     sshpass -p {PASS} ssh -o StrictHostKeyChecking=no -C -D 0.0.0.0:{LOCAL_PORT} -p 31222 root@153.125.231.179
#   to
#     ssh -p 31222 root@153.125.231.179
#

import re
import sys

socksa = 'sshpass -p {PASS} ssh -o StrictHostKeyChecking=no -C -D 0.0.0.0:{LOCAL_PORT} -p 31222 root@seaof-153-125-231-179.jp-tokyo-02.arukascloud.io'
socksb = 'sshpass -p {PASS} ssh -o StrictHostKeyChecking=no -C -D 0.0.0.0:{LOCAL_PORT} -p 31222 root@153.125.231.179'

socks = socksa if len(sys.argv) > 1 else socksb

text1 = re.sub(r'.*\s+-p\s+(\d+)\s*.*\s*root@(\d{1,3}).(\d{1,3}).(\d{1,3}).(\d{1,3}).*\s*', r'ssh -p \1 root@\2.\3.\4.\5', socks)
text2 = re.sub(r'.*\s+-p\s+(\d+)\s*.*\s*root@\w*?-(\d{1,3})-(\d{1,3})-(\d{1,3})-(\d{1,3}).*\s*', r'ssh -p \1 root@\2.\3.\4.\5', socks)

pattern = re.compile(r'.*\s+-p\s+(\d+)\s*.*\s*root@((\d{1,3}).(\d{1,3}).(\d{1,3}).(\d{1,3})|\w*?-(\d{1,3})-(\d{1,3})-(\d{1,3})-(\d{1,3}).*)\s*')
text3 = pattern.sub(r'ssh -p \1 root@\3\7.\4\8.\5\9.\6\10', socks)

text4 = re.sub(r'.*\s+-p\s+(\d+)\s*.*\s*root@((\d{1,3}).(\d{1,3}).(\d{1,3}).(\d{1,3})|\w*?-(\d{1,3})-(\d{1,3})-(\d{1,3})-(\d{1,3}).*)\s*', r'ssh -p \1 root@\3\7.\4\8.\5\9.\6\10', socks)

print("ip  ", text1 == socks, '\t', text1)
print("url ", text2 == socks, '\t', text2)
print("mix ", text3 == socks, '\t', text3)
print("mix ", text4 == socks, '\t', text4)

print("raw ", True, '\t', socks)

