#!/usr/bin/python
# coding=utf-8
# -*- encoding: utf-8 -*-

import sys
import codecs
import os

if __name__ == '__main__':
	# FIXME: The follwing line conflicts with raw_input :(
	# sys.stdin = codecs.getreader('utf-8')(sys.stdin)
	sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
	sys.stderr = codecs.getwriter('utf-8')(sys.stderr)
	
	if len(sys.argv) < 3:
		print 'python split-expand.py <input.expand> <output-dir>'
		print 'e.g. python split-expand.py vblex.expand verb-expand-folder'
		sys.exit(1)
	
	response = raw_input('This script will remove all files in \'' + sys.argv[2] + '\'. Do you want to continue (y/N)?: ')
	if response.strip() != 'Y' and response.strip() != 'y':
		sys.exit(1)
	print 'Deleting all expand files in ', sys.argv[2]
	os.system('rm -f '+ sys.argv[2] + '/*.expand ' +  sys.argv[2] +'/filelist.txt')
	
	groups = {}
	print 'Reading source file'
	with codecs.open(sys.argv[1], 'r', 'utf-8') as file:
		# lines = map(lambda x: x.strip(), file.readlines())
		lines = file.readlines()
	
	for line in lines:
		lemma = line[line.index(':')+1:line.index('<')]
		pos = line[line.index('<')+1:line.index('>')]
		id = lemma + ':' + pos
		if id not in groups.keys(): groups[id] = []
		groups[id].append(line)
	
	filelist = []
	i = 0
	print 'Writing output files'
	for id in groups.keys():
		filename = sys.argv[2].strip('/') + '/' + str(i) + '.expand'
		filelist.append(filename + ' -> ' + id + '\n')
		with codecs.open(filename,'w', 'utf-8') as file:
			file.writelines(groups[id])
		i += 1
	with codecs.open(sys.argv[2].strip('/') + '/' + 'filelist.txt', 'w', 'utf-8') as file:
		file.writelines(filelist)