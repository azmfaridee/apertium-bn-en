#! /usr/bin/env python
# coding=utf-8
# -*- encoding: utf-8 -*-

import sys, string, codecs;
from xml.dom import minidom;
#from xml import xpath;

sys.stdin = codecs.getreader('utf-8')(sys.stdin);
sys.stdout = codecs.getwriter('utf-8')(sys.stdout);
sys.stderr = codecs.getwriter('utf-8')(sys.stderr);

def mangle_flexion_tags(a): #{
	a = a.replace('ind', 'd1');
	a = a.replace('def', 'd2');

	a = a.replace('mf', 'a4');
	a = a.replace('m', 'a1');
	a = a.replace('f', 'a2');
	a = a.replace('nt', 'a3');

	a = a.replace('sg', 'n1');
	a = a.replace('sg', 'n4');
	a = a.replace('du', 'n2');
	a = a.replace('pl', 'n3');

	a = a.replace('nom', 'c1');
	a = a.replace('gen', 'c2');
	a = a.replace('dat', 'c3');
	a = a.replace('acc', 'c4');
	a = a.replace('loc', 'c5');
	a = a.replace('Ins', 'c6');
	a = a.replace('voc', 'c7');

	return a;
#}

def demangle_flexion_tags(a): #{
	a = a.replace('d1', 'ind');
	a = a.replace('d2', 'def');

	a = a.replace('a4', 'mf');
	a = a.replace('a1', 'm');
	a = a.replace('a2', 'f');
	a = a.replace('a3', 'nt');

	a = a.replace('n1', 'sg');
	a = a.replace('n2', 'du');
	a = a.replace('n3', 'pl');
	a = a.replace('n4', 'ct');

	a = a.replace('c1', 'nom');
	a = a.replace('c2', 'gen');
	a = a.replace('c3', 'dat');
	a = a.replace('c4', 'acc');
	a = a.replace('c5', 'loc');
	a = a.replace('c6', 'ins');
	a = a.replace('c7', 'voc');

	return a;
#}

def sort_flexions(a, b): #{

	if(mangle_flexion_tags(a[1]) > mangle_flexion_tags(b[1])): #{
		return 1;
	#}

	if(mangle_flexion_tags(a[1]) == mangle_flexion_tags(b[1])): #{
		return 0;
	#}

	return -1;
#}


# lemma    ;  surface form       ;  symbols                  ;  part-of-speech
# uttanbíggjamaður;  uttanbíggjamenninir;  definite, plural, nominative;  noun, masculine

def find_longest_common_substring(lemma, flexion): #{
        candidate = '';
        length = len(lemma.decode('utf-8'));
        for char in lemma.decode('utf-8'): #{
                candidate = candidate + char;
                if flexion.find(candidate.encode('utf-8')) == -1: #{
                        return candidate[0:len(candidate)-1];
                #}
        #}

        return candidate;
#}

# returns the shortest string from a given list
def return_shortest(ilist): #{

        if len(ilist) == 0: #{
                return -1;
        #}

        return sorted(ilist, key=len)[0]
#}

def return_symlist(symlist): #{
        symlist = symlist.replace(':', '.');
        output = '';

        for symbol in symlist.split('.'): #{
                output = output + '<s n="' + symbol + '"/>';
        #}

        return output;
#}


#
#       MAIN
#

if len(sys.argv) < 2: #{
        print 'python speling.py <filename>';
#}

flist = file(sys.argv[1]);
list = flist.readlines();

current_lemma = '';

lemmata = {};
category = {};
flexions = {};

for line in list: #{

        if len(line) < 2: #{
                continue;
        #}
        row = line.split(';');
        lemma = row[0].strip();

        current_lemma = lemma;
        if current_lemma not in lemmata: #{
                lemmata[current_lemma] = {};
        #}
        if current_lemma not in flexions: #{
                flexions[current_lemma] = {};
        #}
	if current_lemma not in category: #{
		category[current_lemma] = {};
	#}

        inflection = row[1].strip();
#	if lemma.decode('utf-8').islower(): #{
#		inflection = inflection.decode('utf-8').lower().encode('utf-8');
#	#}
	#print lemma , ' / ' , inflection;
        full = inflection;
        stem = find_longest_common_substring(lemma, inflection);
        pos = row[3].strip();
        syms = row[2].strip();
        symlist = pos + ':' + syms;

        #print lemma , '; ' , stem , '; -' + inflection , '; ' , full , '; ' + pos + '; ' + syms;

        form = (inflection, symlist);

	if pos not in lemmata[current_lemma]: #{
		lemmata[current_lemma][pos] = [];
	#}
	if pos not in flexions[current_lemma]: #{
		flexions[current_lemma][pos] = [];
	#}
	if pos not in category[current_lemma]: #{
		category[current_lemma][pos] = '';
	#}

	if form not in flexions[current_lemma][pos]: #{
        	lemmata[current_lemma][pos].append(stem);
		flexions[current_lemma][pos].append(form);
		#category[current_lemma][pos] = pos.split('.')[0];
		category[current_lemma][pos] = pos.replace('.', '_');
	#}

#}

print '<dictionary>';
print '  <pardefs>';

for lemma in lemmata.keys(): #{
	for pos in lemmata[lemma].keys(): #{
	        stem = return_shortest(lemmata[lemma][pos]);
		#print lemma.decode('utf-8')
		#print stem
	        print '  <!-- ' + lemma.decode('utf-8') + '; ' + stem + ' -->';
	        end = lemma.decode('utf-8').replace(stem, '');
	        slash = '/';

	        if end == '': #{
	                slash = '';
	        #}

	        print '    <pardef n="' + stem + slash + end + '__' + category[lemma][pos] + '">';

		flexions[lemma][pos].sort(sort_flexions);

	        for pair in flexions[lemma][pos]: #{
	                print '      <e>';
	                print '        <p>';
	                if len(pair[0]) > 1: #{
	                        print '          <l>' + pair[0].decode('utf-8').replace(stem, '', 1).replace(' ', '<b/>') + '</l>';
	                #}
	                if len(pair[0]) == 1: #{
	                        print '          <l>' + pair[0].decode('utf-8').replace(' ', '<b/>') + '</l>';
	                #}
	                if len(pair[0]) < 1: #{
	                        print '          <l/>';
	                #}
	                print '          <r>' + end + return_symlist(pair[1]) + '</r>';
	                print '        </p>';
	                print '      </e>';
	        #}
	        print '    </pardef>';
	        print '';
	#}
#}
print '  </pardefs>';
print '  <section id="main" type="standard">';

for lemma in lemmata.keys(): #{
	for pos in lemmata[lemma].keys(): #{
	        stem = return_shortest(lemmata[lemma][pos]);
	        end = lemma.decode('utf-8').replace(stem, '');
	        slash = '/';

	        if end == '': #{
	                slash = '';
	        #}

            # spectie, I belive this was the problem we were keeping the space, whereas it should be replaced by </b>, what do you think?
	        #print '    <e lm="' + lemma.decode('utf-8') + '"><i>' + stem + '</i><par n="' +  stem + slash + end + '__' + category[lemma][pos] + '"/></e>';
	        print '    <e lm="' + lemma.decode('utf-8') + '"><i>' + stem.replace(' ', '<b/>') + '</i><par n="' +  stem + slash + end + '__' + category[lemma][pos] + '"/></e>';
	#}
#}

print '  </section>';
print '</dictionary>';

