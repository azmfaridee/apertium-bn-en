#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

with open('/tmp/fresh.noun','w') as f:	pass
with open('/tmp/fresh.proper-noun','w') as f:	pass
with open('/tmp/fresh.adj','w') as f:	pass

POSMAP = {}
POSMAP['n'] = '/tmp/fresh.noun'
POSMAP['np'] = '/tmp/fresh.proper-noun'
POSMAP['adj'] = '/tmp/fresh.adj'

for i in sys.stdin:
	line = i.split()
	pos = line[1].split(',')
	#print line[0], '-', pos
	for p in pos:
		with open(POSMAP[p],'a') as f:
			f.write(line[0]+'\n')
