#!/usr/bin/python
# coding=utf-8
# -*- encoding: utf-8 -*-

# use this script to create svn friendly mysql dump files, each
# insert value in one of the lines

import sys, codecs

lines = []

for line in sys.stdin: lines.append(line.strip().decode('utf-8'))

for line in lines:
	if line.startswith('INSERT INTO'):
		main = line[:line.index('VALUES')+len('VALUES')].strip()
		print main
		rest = line[line.index(main)+len(main):].strip().split('),(')
		for index, data in enumerate(rest):
			if data.startswith('('): data = data.replace('(', '', 1)
			if data.endswith(');'): data = data.replace(');', '', 1)
			data = u'(' + data.strip() + u')'			
			if index == len(rest) - 1: data += u';'
			else: data += u','
			print data.encode('utf-8')
	else:
		print line.encode('utf-8')
		