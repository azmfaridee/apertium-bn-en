#!/usr/bin/python2.5
# coding=utf-8
# -*- encoding: utf-8 -*-

import sys, codecs, copy, Ft;
from Ft.Xml.Domlette import NonvalidatingReader;
from Ft.Xml.XPath import Evaluate;

#from xml.dom import minidom;
#from xml import xpath;

sys.stdout = codecs.getwriter('utf-8')(sys.stdout);
sys.stderr = codecs.getwriter('utf-8')(sys.stderr);

sys.setrecursionlimit(20000);

dictionary = sys.argv[1];

doc = NonvalidatingReader.parseUri('file:///' + dictionary);
path = '/dictionary/pardefs/pardef';

paradigms = {};

# Convert from a dotted symbol list into a list of 
# symbols in XML:
#
# n.m.sg --> <s n="n"/><s n="m"/><s n="sg"/>
#

def return_symlist(symlist): #{
	if len(symlist) < 1: #{
		return '';
	#}
	if symlist[0] == '.': #{
		symlist = symlist[1:];
	#}
	symlist = symlist.replace(':', '.');
	output = '';

	for symbol in symlist.split('.'): #{
		output = output + '<s n="' + symbol + '"/>';
	#}

	return output;
#}

# Return the string between the slash and the underscore.
# e.g. m/an__n --> "an"
#

def roll_right(name): #{
	bar_idx = name.find(u'/') + 1;
	udr_idx = name.find(u'_');

	rstring = name[bar_idx:udr_idx];

	if name.find('/') == -1: #{
		rstring = '';
	#}
	
	return rstring;	
#}

# Compare two paradigms
#
# Returns '1' if they are equivalent, '0' if they are not.
#
def compare_paradigms(paradigm1, paradigm2): #{
	# paradigm,stem,symbols !! paradigm,stem,symbols	
	common = 0;

	if len(paradigm1) != len(paradigm2): #{
		return 0;
	#}

	for pair1 in paradigm1: #{
		for pair2 in paradigm2: #{
			if pair1[0] == pair2[0] and pair1[1] == pair2[1]: #{
				common = common + 1;
			#}
		#}
	#}

	if common == len(paradigm1): #{
		return 1;
	#}
		
	return 0;
#}

# Compare the length of two strings
#
# Returns: -1 (a < b), 0 (a == b), 1 (a > b)
#
def string_length_compare(a, b): #{
	if len(a) == len(b): #{
		return 0;
	#}
	if len(a) > len(b): #{
		return 1;
	#}

	return -1;
#}

# Does a duplicate paradigm exist, that is, given an existing
# list of paradigms, do either of the two
def duplicate_exists(p1, p2, duplicates): #{
	for potential in duplicates.keys(): #{
		for potential2 in duplicates[potential]: #{
			if p1 == potential or p1 == potential2: #{
				return 1;
			#}
		#}
	#} 

	return 0;
#}

count = 0;

#
# Build the list of paradigms
# 

# For each paradigm definition in the pardefs section
for node in Ft.Xml.XPath.Evaluate(path, contextNode=doc): #{
        pardef = node.getAttributeNS(None, 'n');

	if pardef not in paradigms: #{
		# Create a new list for the suffix/symbol tuples
		paradigms[pardef] = [];
	#}

	count = count + 1;
	if count % 1000 == 0: #{
		print >> sys.stderr, count , pardef;
	#}

	# For each entry <e> in the paradigm,
	for child in Ft.Xml.XPath.Evaluate('.//e', contextNode=node): #{
		# For each pair <p> in the entry,
		for pair in Ft.Xml.XPath.Evaluate('.//p', contextNode=child): #{
			suffix = '';
			# The left side <l> is the text between <l></l>
			left = Ft.Xml.XPath.Evaluate('.//l', contextNode=pair)[0].firstChild;

			if type(left) != type(None): #{
				suffix = left.nodeValue;
			else: #{
				suffix = ''
			#}

			symbols = '';
			# The right side <r> is the list of symbols
			right =  Ft.Xml.XPath.Evaluate('.//r', contextNode=pair)[0];
			for sym in Ft.Xml.XPath.Evaluate('.//s', contextNode=right): #{
				symbol = '';
				if type(sym) != type(None): #{
					symbol = sym.getAttributeNS(None, 'n');
				#}
				symbols = symbols + '.' + symbol;
			#}

			p = (suffix, symbols);

			# Add the tuple of suffix and symbols to the paradigm
			# e.g. for the noun `pan' the following tuples:
			#        ('es', 'n.m.pl'), ('', 'n.m.sg')

			paradigms[pardef].append(p);
		#}
	#}
#}

sorted_paradigms = [];

for item in paradigms.keys(): #{
	sorted_paradigms.append(item);
#}

# Sort the list of paradigms by the length of the name
# of the paradigm, this allows us to take the "shortest"
# name for the paradigm which is kept.
sorted_paradigms.sort(string_length_compare);

# Each entry in this hash table is a list of duplicate paradigms
# and the key is the name of the paradigm which they are a duplicate of.
duplicates = {};

# Takes a list of paradigms, a hash of duplicates and the 
# paradigm which is currently being processed.
def strip_duplicates(paradigms, duplicates, current): #{
#	print 'paradigms: ' , len(paradigms);
	
	for paradigm1 in paradigms.keys(): #{
		# If the paradigms are the same, move along
		if paradigm1 in paradigms and current in paradigms and current != paradigm1: #{
			# If the current paradigm does not yet have a list of duplicates 
			# associated with it, create the list.
			if current not in duplicates: #{
				duplicates[current] = [];
			#}

			# If the two paradigms are equivalent in suffix/symbol pairs and the text section
			# in between the / and the _ is the same, then we consider them equal.
			if compare_paradigms(paradigms[paradigm1], paradigms[current]) == 1 and roll_right(paradigm1) == roll_right(current): #{
#				print paradigms[paradigm1] , '; ' , paradigms[current];

				# paradigm1 is a duplicate of current paradigm, add
				# paradigm1 to the duplicate list for current.
				duplicates[current].append(paradigm1);
				
				# Remove the paradigm we just added a duplicate of, this means
				# that each time we find a duplicate paradigm, we reduce the 
				# search space.
				del paradigms[paradigm1];

				# Recurse
				strip_duplicates(paradigms, duplicates, current);
			#}
		#}
	#}
	return;
#}

#z = copy.deepcopy(paradigms);

# For each paradigm 'k' in the name length sorted list
# of paradigms,
for k in sorted_paradigms: #{
	print >> sys.stderr, k;
	# Recurse down through the paradigms.
	strip_duplicates(paradigms, duplicates, k);
#}

print >> sys.stderr, 'Paradigms: ' , len(paradigms);

print >> sys.stderr, '---';

# Print out new dictionary and pardefs section.
print '<dictionary>';
print '  <pardefs>';
for paradigm in paradigms.keys(): #{
	bar_idx = paradigm.find(u'/') + 1;
	udr_idx = paradigm.find(u'_');

	print '    <pardef n="' + paradigm + '">';
	for pair in paradigms[paradigm]: #{
		print '      <e>';
		print '        <p>';
		if pair[0] == type(None): #{
			print '          <l/>';
		else: #{
			print('          <l>%s</l>' % (pair[0]));
		#}
		rpost = paradigm[bar_idx:udr_idx];
		if paradigm.find('/') == -1: #{
			rpost = '';
		#}
		print '          <r>' + rpost + return_symlist(pair[1]) + '</r>';
		print '        </p>';
		print '      </e>';
	#}
	print '    </pardef>';
#}
print '  </pardefs>';
print '  <section id="main" type="standard">';

d = file(dictionary);

output = '';
for line in d.readlines(): #{
        if line.count('<e lm="') > 0: #{
		output = output + line;
        #}

#}

# For each paradigm in the hash of duplicates, take the list for
# each one and replace each item in the list with the name of the 
# paradigm as the key.
total = 0;
for paradigm in duplicates.keys(): #{
	for p in duplicates[paradigm]: #{
		print >> sys.stderr, '+ ' , p , u' → ' , paradigm;
		output = output.replace('n="' + p + '"', 'n="' + paradigm + '"');
	#}
	total = total + len(duplicates[paradigm]) + 1;
#}

print output;

print '  </section>';
print '</dictionary>';


print >> sys.stderr, '---';
print >> sys.stderr, 'duplicates: ' , len(duplicates) , '; total: ' , total;
print >> sys.stderr, 'paradigms: ' , len(paradigms);
#print >> sys.stderr, 'z: ' , len(z);
