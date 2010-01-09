#!/usr/bin/python
# coding=utf-8
# -*- encoding: utf-8 -*-

# This script is useful when the content of the files are relevant but the order
# in which they appear in the files are different and sorting them is not an
# option

import sys
import codecs

if __name__ == '__main__':
	sys.stdin = codecs.getreader('utf-8')(sys.stdin)
	sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
	sys.stderr = codecs.getwriter('utf-8')(sys.stderr)

	if len(sys.argv) < 3:
		print 'python relaxed-diff.py file1 file2'
		sys.exit(1)

	with codecs.open(sys.argv[1], 'r', 'utf-8') as file:
		file1 = map(lambda x: x.strip(), file.readlines())
	with codecs.open(sys.argv[2], 'r', 'utf-8') as file:
		file2 = map(lambda x: x.strip(), file.readlines())

	for x in file1:
		if x not in file2: print '+%s: %s' % (sys.argv[1], x)

	for x in file2:
		if x not in file1: print '+%s: %s' % (sys.argv[2], x)