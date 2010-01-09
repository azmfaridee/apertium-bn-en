#!/usr/bin/python
# coding=utf-8
# -*- encoding: utf-8 -*-

import sys
import codecs
import re
from pprint import pprint


# line buffer
lines = []

lemmata = {}
categories = {}
flexions = {}

# recursive lambda definition for longest common substring
# get_longest_common_substring = lambda a, b: b.find(a) == -1 and get_longest_common_substring(a[:-1], b) or a
get_longest_common_substring = lambda a, b: get_longest_common_substring(a[:-1], b) if b.find(a) == -1 else a

# lambda definition to get the shortest lemma from a list
get_shortest = lambda list: -1 if len(list) == 0 else sorted(list, key=len)[0]

# get pos from a symbol string
# the symbol string will be in 'np_mf_nn_sg_nom' format
# we want the first tag (and sometimes with the second one depending on the pos)
def get_pos(symbol):
	if symbol.startswith('np_') or symbol.startswith('n_'): return reduce(lambda x, y: x + '_' + y, symbol.split('_')[:2])
	if symbol.startswith('vblex') or symbol.startswith('cnjcoo') or symbol.startswith('num') or symbol.startswith('det') or symbol.startswith('prn') or symbol.startswith('post') or symbol.startswith('adv') or symbol.startswith('adj'): return symbol.split('_')[0]

# create symbol list from the xml dix
def get_symlist(symlist):
	symlist = symlist.replace(':', '_')
	output = ''
	for symbol in symlist.split('_'): output += '<s n="' + symbol + '"/>'
	return output

# main program
if __name__ == '__main__':
	# cast the input and output streams so that they can read and write unicode
	# compliant charactes properly
	sys.stdin = codecs.getreader('utf-8')(sys.stdin)
	sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
	sys.stderr = codecs.getwriter('utf-8')(sys.stderr)

	# append each line from stdin to line buffer
	for line in sys.stdin:
		lines.append(line.strip())

	for line in lines:
		# FIXME: right now we are not dealing REGEX
		if line.startswith('__REGEXP__'): continue
		
		# ignore comments
		# NOTE: normal expand files do not contain comments, but one can leave
		# commented regions when editing them afterwared
		if line.startswith('#'): continue

		# seperate inflection and lemma
		inflection, lemma_with_symbol = line.split(':')

		# seperate lemma from enclitics
		if lemma_with_symbol.find('+') != -1:
			lemma_base, enclitic = lemma_with_symbol.split('+')
			enclitic = enclitic[:enclitic.find('<')], enclitic[enclitic.find('<'):].replace('><', '_').lstrip('<').rstrip('>')
		else:
			lemma_base, enclitic = lemma_with_symbol, None

		# create the original lemma
		lemma = lemma_base[:lemma_base.find('<')]

		# seperate the stem by taking the longest common substring among lemma and inflection
		stem = get_longest_common_substring(lemma, inflection)

		# seperate the total symbols
		symbols = lemma_base[lemma_base.find('<'):].replace('><', '_').lstrip('<').rstrip('>')

		# get the pos from symbols
		pos = get_pos(symbols)

		# get other tags
		# FIXME: symbols.lstrip(pos+')') does not work, why?
		tag = symbols.replace(pos, '').lstrip('_')

		# generate the form, that will be saved in the flexion databse
		if tag == '': form = inflection, pos, enclitic
		else: form = inflection, pos + ':' + tag, enclitic

		# DEBUG
# 		print >> sys.stderr, 'lemma', lemma.encode('utf-8')
# 		print >> sys.stderr, 'inflection', inflection.encode('utf-8')
# 		print >> sys.stderr, 'pos', pos.encode('utf-8')
# 		print >> sys.stderr, 'tag', tag.encode('utf-8')
# 		if enclitic != None: print >> sys.stderr, 'enclitic', enclitic

		if lemma not in lemmata: lemmata[lemma] = {}
		if lemma not in flexions: flexions[lemma] = {}
		if lemma not in categories: categories[lemma] = {}

		if pos not in lemmata[lemma]: lemmata[lemma][pos] = []
		if pos not in flexions[lemma]: flexions[lemma][pos] = []
		if pos not in categories[lemma]: categories[lemma][pos] = ''

		if form not in flexions[lemma][pos]:
			lemmata[lemma][pos].append(stem)
			flexions[lemma][pos].append(form)
			categories[lemma][pos] = pos

	# DEBUG
# 	pprint(lemmata, sys.stderr)
# 	pprint(flexions, sys.stderr)
# 	pprint(categories, sys.stderr)

	print '<dictionary>'
	print '  <pardefs>'
	for lemma in lemmata.keys():
		for pos in lemmata[lemma].keys():
			stem =  get_shortest(lemmata[lemma][pos])

			# print '  <!-- ' + lemma.encode('utf-8') + '; ' + stem.encode('utf-8') + ' -->'
			print '  <!-- ' + lemma + '; ' + stem + ' -->'

			end = lemma.lstrip(stem)
			if end == '': slash = ''
			else: slash = '/'

			print '    <pardef n="' + stem + slash + end + '__' + categories[lemma][pos] + '">'

			# FIXME: this is where we are supposed to sort the flexions, I supposed we can skip that for now
			for pair in flexions[lemma][pos]:
				# DEBUG
# 				print >> sys.stderr, 'pair', pair

				print '      <e>'
				print '        <p>'
				if len(pair[0]) > 1:
					print '          <l>' + pair[0].replace(stem, '', 1).replace(' ', '<b/>') + '</l>'
				elif len(pair[0]) == 1:
					print '          <l>' + pair[0].replace(' ', '<b/>') + '</l>'
				else:
					print '          <l/>'

				#	append enclitics
				if pair[2] == None:	enclitic = ''
				else: enclitic = '<j/>' + pair[2][0] + get_symlist(pair[2][1])
				print '          <r>' + end + get_symlist(pair[1]) + enclitic +'</r>'
				print '        </p>'
				print '      </e>'
		print '    </pardef>'
		print ''
	print '  </pardefs>'
	print '  <section id="main" type="standard">'
	for lemma in lemmata.keys():
		for pos in lemmata[lemma].keys():
			stem = get_shortest(lemmata[lemma][pos])
			end = lemma.lstrip(stem)
			if end == '': slash = ''
			else: slash = '/'
			print '    <e lm="' + lemma + '"><i>' + stem.replace(' ', '<b/>') + '</i><par n="' +  stem + slash + end + '__' + categories[lemma][pos] + '"/></e>'
	print '  </section>'
	print '</dictionary>'
