#!/usr/bin/python2.5
# coding=utf-8
# -*- encoding: utf-8 -*-

# The default shell utility 'uniq' does not support unicode, use this one istead
import sys
entries = []
for e in sys.stdin:
	e = e.strip()
	if e not in entries:
		entries.append(e)
for e in entries:
	print >> sys.stdout, e
