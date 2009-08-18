#!/usr/bin/python
# coding=utf-8
# -*- encoding: utf-8 -*-

import sys, codecs, copy;
from xml.dom import minidom;
from xml import xpath;

sys.stdout = codecs.getwriter('utf-8')(sys.stdout);
sys.stderr = codecs.getwriter('utf-8')(sys.stderr);

if len(sys.argv) < 2: #{
	print 'python apertium2extract.py <dix file>';
	sys.exit(-1);
#}

dictionary = sys.argv[1];

doc = minidom.parse(dictionary).documentElement;
path = '/dictionary/pardefs/pardef';

paradigms = {};
categories = ['__n', '__adj', '__vblex'];

for node in xpath.Evaluate(path, doc): #{
        pardef = node.getAttribute('n');

	if pardef not in paradigms: #{
		paradigms[pardef] = [];
	#}
	selected = 0;
	for category in categories: #{
		if pardef.count(category) > 0: #{
			selected = 1;
		#}
	#}

	if selected < 1: #{
		continue;
	#}

	for child in node.getElementsByTagName('e'): #{
		for pair in child.getElementsByTagName('p'): #{
			suffix = '';
			left = pair.getElementsByTagName('l')[0].firstChild;

			if type(left) != type(None): #{
				suffix = left.nodeValue;
			#}

			if type(suffix) == type(None): #{
				suffix = '';
			#}

			symbols = '';
			for sym in pair.getElementsByTagName('r')[0].getElementsByTagName('s'): #{
				symbol = '';
				if type(sym) != type(None): #{
					symbol = sym.getAttribute('n');
				#}
				symbols = symbols + '.' + symbol;
			#}

			paradigms[pardef].append(suffix);
		#}
	#}
#}

universal_set = []

for paradigm in paradigms.keys(): #{
	for p in paradigms[paradigm]: #{
		universal_set.append(p);
	#}
#}

universal_set = set(universal_set);

for paradigm in paradigms.keys(): #{
	#paradigm rna__vblex = 
	#        x
	#        { x+"ð" & x+"ði" & x+"ðu" & x+"ður" & x+"r" & ~(x+"dur" | x+"t")} ;

#	if paradigm.count('/') > 0: #{
		#continue;
	#}
	lset = len(set(paradigms[paradigm]));
	if lset < 2: #{
		continue;
	#}

	print '-- ' + paradigm; 
#	print 'paradigm ' + paradigm.encode('ascii', 'ignore') + ' =';	
	print 'paradigm ' + paradigm + ' =';
	print '\t' + 'x {';

	stems = '\t\t';
	count = 0;
	idx = 0;
	for pair in set(paradigms[paradigm]): #{
		if len(pair) >= 1: #{
			add = 'x+"' + pair + '" ';
			if idx != lset-1: #{
				add = 'x+"' + pair + '" & ';
			#}
			stems = stems + add;
		#}

		if count == 6 and count != lset -1: #{
			stems = stems + '\n\t\t';
			count = 0;
		#}
		count = count + 1;
		idx = idx + 1;
	#}
	complement = universal_set - set(paradigms[paradigm]);
	stems = stems + ' & \n\t\t~(';
	count = 0;
	for s in complement: #{
		stems = stems + 'x+"' + s + '" | ';
		if count == 6 and count != lset -1: #{
			stems = stems + '\n\t\t';
			count = 0;
		#}
		count = count + 1;
	#}
	stems = stems + ')\t' + '};';	
	print stems.replace('| )', ')').replace('| \n\t\t)', ')');
	print '';
#}
