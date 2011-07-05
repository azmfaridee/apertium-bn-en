#!/usr/bin/env python
# -*- coding: utf-8 -*-

# INPUT: 	lemma<comma>pardefid	where pardefid is defined in 'proper-noun.pardef'
# OUTPUT:	monodix entry strings for the  given lemma with appropriate pardef mapping
# note: 	this output is used by 'tag-proper-noun.sh'

import sys, re

table = {}
tag = {}
template = "    <e lm=\"xxx\"><i>xxx</i><par n=\"yyy__np_|\"/></e>"

#load adjective pardef table
with open('proper-noun.pardefs','r') as f:
	for line in f:
		if line == '\n':
			continue
		
		pd = line.strip().split(',')
		par = pd[1].split()
		table[par[0]] = pd[0]
		tgs = par[1].split('>')
		tag[par[0]] = re.sub('<','',tgs[1])

#process new words
for i in sys.stdin:
	line = i.strip().split(',')
	temp = re.sub('yyy',table[line[1]],re.sub('xxx',line[0],template))
	t = temp.split('|')
	print t[0] + tag[line[1]] + t[1]
