#!/usr/bin/python
# coding=utf-8
# -*- encoding: utf-8 -*-

import sys
import codecs
import re
# for debugging
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
	if symbol.startswith(u'np_') or symbol.startswith(u'n_'): return reduce(lambda x, y: x + u'_' + y, symbol.split(u'_')[:2])
	if symbol.startswith(u'vblex_') or symbol.startswith(u'cnjcoo_') or symbol.startswith(u'num_') or symbol.startswith(u'det_') or symbol.startswith(u'prn_') or symbol.startswith(u'post_') or symbol.startswith(u'adv_') or symbol.startswith(u'adj_'): return symbol.split(u'_')[0]

# create symbol list from the xml dix
def get_symlist(symlist):
	symlist = symlist.replace(u':', u'_')
	output = u''
	for symbol in symlist.split(u'_'): output += u'<s n="' + symbol + u'"/>'
	return output

# main program
if __name__ == '__main__':
	# append each line from stdin to line buffer
	for line in sys.stdin:
		lines.append(line.strip().decode('utf-8'))

	for line in lines:
		# seperate inflection and lemma
		inflection, lemma_with_symbol = line.split(u':')

		# seperate lemma from enclitics
		if lemma_with_symbol.find(u'+') != -1:
			lemma_base, enclitic = lemma_with_symbol.split(u'+')
			enclitic = enclitic[:enclitic.find(u'<')], enclitic[enclitic.find(u'<'):].replace(u'><', u'_').lstrip(u'<').rstrip(u'>')
		else:
			lemma_base, enclitic = lemma_with_symbol, None

		# create the original lemma
		lemma = lemma_base[:lemma_base.find(u'<')]

		# seperate the stem by taking the longest common substring among lemma and inflection
		stem = get_longest_common_substring(lemma, inflection)

		# seperate the total symbols
		symbols = lemma_base[lemma_base.find(u'<'):].replace(u'><', u'_').lstrip(u'<').rstrip(u'>')

		# get the pos from symbols
		pos = get_pos(symbols)

		# get other tags
		# FIXME: symbols.lstrip(pos+')') does not work, why?
		tag = symbols.replace(pos, '').lstrip('_')

		# generate the form, that will be saved in the flexion databse
		form = inflection, pos + u':' + tag, enclitic

		# DEBUG
		# print lemma, inflection, pos, tag, enclitic

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
# 	pprint(lemmata)
# 	pprint(flexions)
# 	pprint(categories)

	print '<dictionary>'
	print '  <pardefs>'
	for lemma in lemmata.keys():
		for pos in lemmata[lemma].keys():
			stem =  get_shortest(lemmata[lemma][pos])

			print '  <!-- ' + lemma.encode('utf-8') + '; ' + stem.encode('utf-8') + ' -->'

			end = lemma.lstrip(stem)
			if end == u'': slash = ''
			else: slash = '/'

			print '    <pardef n="' + stem.encode('utf-8') + slash + end.encode('utf-8') + '__' + categories[lemma][pos].encode('utf-8') + '">'

			# FIXME: this is where we are supposed to sort the flexions, I supposed we can skip that for now
			for pair in flexions[lemma][pos]:
				print '      <e>'
				print '        <p>'
				if len(pair[0]) > 1:
					print '          <l>' + pair[0].replace(stem, u'', 1).replace(u' ', u'<b/>').encode('utf-8') + '</l>'
				elif len(pair[0] == 1):
					print '          <l>' + pair[0].replace(u' ', u'<b/>').encode('utf-8') + '</l>'
				else:
					print '          <l/>'

				#	append enclitics
				if pair[2] == None:	enclitic = ''
				else: enclitic = '<j/>' + pair[2][0] + get_symlist(pair[2][1])
				print '          <r>' + end.encode('utf-8') + get_symlist(pair[1]).encode('utf-8') + enclitic.encode('utf-8') +'</r>'
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
			if end == u'': slash = ''
			else: slash = '/'
			print '    <e lm="' + lemma.encode('utf-8') + '"><i>' + stem.replace(' ', '<b/>').encode('utf-8') + '</i><par n="' +  stem.encode('utf-8') + slash.encode('utf-8') + end.encode('utf-8') + '__' + categories[lemma][pos].encode('utf-8') + '"/></e>'
	print '  </section>'
	print '</dictionary>'
