#!/usr/bin/env python
# -*- coding: utf-8 -*-

# INPUT: 	lemma<comma>pardefid	where pardefid is defined in 'nadj.pardef'
# OUTPUT:	monodix entry strings for the  given lemma with appropriate pardef mapping
# note: 	this output is used by 'tag-adj.sh'

import sys, re

table = {}
template = "    <e lm=\"xxx\"><i>xxx</i><par n=\"yyy__adj\"/></e>"

#load adjective pardef table
with open('adj.pardefs','r') as f:
	for line in f:
		if line == '\n':
			continue
		pd = line.strip().split(',')
		par = pd[1].split()
		table[par[0]] = pd[0]

#process new words
for i in sys.stdin:
	line = i.strip().split(',')
	print re.sub('yyy',table[line[1]],re.sub('xxx',line[0],template))
