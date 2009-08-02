#!/usr/bin/python2.6
# coding=utf-8
# -*- encoding: utf-8 -*-

import os
import sys
import MySQLdb
import re
import pdb
import codecs
from pprint import pprint

V = u'[অআইঈউঊঋএঐওঔ]'
C = u'[কখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়ঁ]'
K = u'[ািীুূৃেৈোৌ]'
	
DEBUG = False

def dprint(str):
    if DEBUG == True:
	print 'DEBUG: ' + str
	
def get_nom(lemma, animacy):
    norm, enc_e, enc_o = [{} for i in range(3)]
    
    regex = V + u'(ঁ)?$'
    if re.search(regex, lemma.decode('utf-8')):
	dprint(lemma + 'V' + animacy)
	if animacy == 'nn':
	    norm = {'sg': '', 'sd': 'টা', 'pl': 'গুলো'}
	elif animacy == 'aa':
	    norm = {'sg': '', 'sd': 'টা', 'pl': 'গুলো'}
	elif animacy == 'hu':
	    norm = {'sg': '', 'sd': 'টা', 'pl': 'রা'}
	elif animacy == 'el':
	    norm = {'sg': '', 'sd': '', 'pl': 'গণ'}
	return norm #, enc_e, enc_o
    
    
    regex = K + u'(ঁ)?$'
    if re.search(regex, lemma.decode('utf-8')):
	dprint(lemma + 'K' + animacy)
	if animacy == 'nn':
	    norm = {'sg': '', 'sd': 'টা', 'pl': 'গুলো'}
	elif animacy == 'aa':
	    norm = {'sg': '', 'sd': 'টা', 'pl': 'গুলো'}
	elif animacy == 'hu':
	    norm = {'sg': '', 'sd': 'টা', 'pl': 'রা'}
	elif animacy == 'el':
	    norm = {'sg': '', 'sd': '', 'pl': 'গণ'}
	return norm #, enc_e, enc_o
    
    regex = C + u'(ঁ)?$'
    if re.search(regex, lemma.decode('utf-8')):
	dprint(lemma + 'C' + animacy)
	if animacy == 'nn':
	    norm = {'sg': '', 'sd': 'টা', 'pl': 'গুলো'}
	elif animacy == 'aa':
	    norm = {'sg': '', 'sd': 'টা', 'pl': 'গুলো'}
	elif animacy == 'hu':
	    norm = {'sg': '', 'sd': 'টা', 'pl': 'রা'}
	elif animacy == 'el':
	    norm = {'sg': '', 'sd': '', 'pl': 'গণ'}
	return norm #, enc_e, enc_o
    
    
    return norm #, enc_e, enc_o

def get_obj(lemma, animacy):
    norm, enc_e, enc_o = [{} for i in range(3)]
    
    regex = V + u'(ঁ)?$'
    if re.search(regex, lemma.decode('utf-8')):
	dprint(lemma + 'V' + animacy)
	if animacy == 'nn':
	    norm = {'sg': '', 'sd': 'টা', 'pl': 'গুলো'}
	elif animacy == 'aa':
	    norm = {'sg': 'কে', 'sd': 'টাকে', 'pl': 'গুলোকে'}
	elif animacy == 'hu':
	    norm = {'sg': 'কে', 'sd': 'টাকে', 'pl': 'দেরকে'}
	elif animacy == 'el':
	    norm = {'sg': 'কে', 'sd': 'কে', 'pl': 'গণকে'}
	return norm #, enc_e, enc_o
    
    
    regex = K + u'(ঁ)?$'
    if re.search(regex, lemma.decode('utf-8')):
	dprint(lemma + 'K' + animacy)
	if animacy == 'nn':
	    norm = {'sg': '', 'sd': 'টা', 'pl': 'গুলো'}
	elif animacy == 'aa':
	    norm = {'sg': 'কে', 'sd': 'টাকে', 'pl': 'গুলোকে'}
	elif animacy == 'hu':
	    norm = {'sg': 'কে', 'sd': 'টাকে', 'pl': 'দেরকে'}
	elif animacy == 'el':
	    norm = {'sg': 'কে', 'sd': 'কে', 'pl': 'গণকে'}
	return norm #, enc_e, enc_o
    
    regex = C + u'(ঁ)?$'
    if re.search(regex, lemma.decode('utf-8')):
	dprint(lemma + 'C' + animacy)
	if animacy == 'nn':
	    norm = {'sg': '', 'sd': 'টা', 'pl': 'গুলো'}
	elif animacy == 'aa':
	    norm = {'sg': 'কে', 'sd': 'টাকে', 'pl': 'গুলোকে'}
	elif animacy == 'hu':
	    norm = {'sg': 'কে', 'sd': 'টাকে', 'pl': 'দেরকে'}
	elif animacy == 'el':
	    norm = {'sg': 'কে', 'sd': 'কে', 'pl': 'গণকে'}
	return norm #, enc_e, enc_o
        
    
    return norm #, enc_e, enc_o

def get_gen(lemma, animacy):
    norm, enc_e, enc_o = [{} for i in range(3)]

    regex = V + u'(ঁ)?$'
    if re.search(regex, lemma.decode('utf-8')):
	dprint(lemma + 'V' + animacy)
	if animacy == 'nn':
	    norm = {'sg': 'য়ের', 'sd': 'টার', 'pl': 'গুলোর'}
	elif animacy == 'aa':
	    norm = {'sg': 'য়ের', 'sd': 'টার', 'pl': 'গুলোর'}
	elif animacy == 'hu':
	    norm = {'sg': 'য়ের', 'sd': 'টার', 'pl': 'দের'}
	elif animacy == 'el':
	    norm = {'sg': 'য়ের', 'sd': 'য়ের', 'pl': 'গণের'}
	return norm #, enc_e, enc_o
    
    
    regex = K + u'(ঁ)?$'
    if re.search(regex, lemma.decode('utf-8')):
	dprint(lemma + 'K' + animacy)
	if animacy == 'nn':
	    norm = {'sg': 'র', 'sd': 'টার', 'pl': 'গুলোর'}
	elif animacy == 'aa':
	    norm = {'sg': 'র', 'sd': 'টার', 'pl': 'গুলোর'}
	elif animacy == 'hu':
	    norm = {'sg': 'র', 'sd': 'টার', 'pl': 'দের'}
	elif animacy == 'el':
	    norm = {'sg': 'র', 'sd': 'র', 'pl': 'গণের'}
	return norm #, enc_e, enc_o
    
    regex = C + u'(ঁ)?$'
    if re.search(regex, lemma.decode('utf-8')):
	dprint(lemma + 'C' + animacy)
	if animacy == 'nn':
	    norm = {'sg': 'ের', 'sd': 'টার', 'pl': 'গুলোর'}
	elif animacy == 'aa':
	    norm = {'sg': 'ের', 'sd': 'টার', 'pl': 'গুলোর'}
	elif animacy == 'hu':
	    norm = {'sg': 'ের', 'sd': 'টার', 'pl': 'দের'}
	elif animacy == 'el':
	    norm = {'sg': 'ের', 'sd': 'ের', 'pl': 'গণের'}
	return norm #, enc_e, enc_o
        
    return norm #, enc_e, enc_o

def get_loc(lemma, animacy):
    norm, enc_e, enc_o = [{} for i in range(3)]
    
    regex = V + u'(ঁ)?$'
    if re.search(regex, lemma.decode('utf-8')):
	dprint(lemma + 'V' + animacy)
	if animacy == 'nn':
	    norm = {'sg': 'য়ে', 'sd': 'টায়', 'pl': 'গুলোয়'}
	elif animacy == 'aa':
	    norm = None
	elif animacy == 'hu':
	    norm = None
	elif animacy == 'el':
	    norm = None
	return norm #, enc_e, enc_o

    regex = u'া(ঁ)?$'
    if re.search(regex, lemma.decode('utf-8')):
	dprint(lemma + 'K' + animacy)
	if animacy == 'nn':
	    norm = {'sg': 'য়', 'sd': 'টায়', 'pl': 'গুলোয়'}
	elif animacy == 'aa':
	    norm = None
	elif animacy == 'hu':
	    norm = None
	elif animacy == 'el':
	    norm = None
	return norm #, enc_e, enc_o    
    
    regex = K + u'(ঁ)?$'
    if re.search(regex, lemma.decode('utf-8')):
	dprint(lemma + 'K' + animacy)
	if animacy == 'nn':
	    norm = {'sg': 'তে', 'sd': 'টায়', 'pl': 'গুলোয়'}
	elif animacy == 'aa':
	    norm = None
	elif animacy == 'hu':
	    norm = None
	elif animacy == 'el':
	    norm = None
	return norm #, enc_e, enc_o
    
    regex = C + u'(ঁ)?$'
    if re.search(regex, lemma.decode('utf-8')):
	dprint(lemma + 'C' + animacy)
	if animacy == 'nn':
	    norm = {'sg': 'ে', 'sd': 'টায়', 'pl': 'গুলোয়'}
	elif animacy == 'aa':
	    norm = None
	elif animacy == 'hu':
	    norm = None
	elif animacy == 'el':
	    norm = None
	return norm #, enc_e, enc_o        
    
    return norm #, enc_e, enc_o
	
def get_inflection(lemma, animacy = 'nn'):
    nom, obj, gen, loc = [{} for i in range (4)]
    '''nom['norm'], nom['enc_e'], nom['enc_o'] = get_nom(lemma, animacy)
    obj['norm'], obj['enc_e'], obj['enc_o'] = get_obj(lemma, animacy)
    gen['norm'], gen['enc_e'], gen['enc_o'] = get_gen(lemma, animacy)
    loc['norm'], loc['enc_e'], loc['enc_o'] = get_loc(lemma, animacy)'''
    nom['norm'] = get_nom(lemma, animacy)
    obj['norm'] = get_obj(lemma, animacy)
    gen['norm'] = get_gen(lemma, animacy)
    loc['norm'] = get_loc(lemma, animacy)
    return nom , obj, gen, loc
    
animacy_table = {'0': 'nn', '1': 'aa', '2': 'hu', '3': 'el'}
gender_table = {'0': 'mf', '1': 'm', '2': 'f', '3': 'nt'}

def get_sym(list):
    sym = ''
    for e in list:
        sym = sym + '<s n="' + e + '"/>'
    return sym

def get_num(data):
    if data == 'sd': return '<s n="sg"/>', '<s n="def"/>'
    else: return '<s n="' + data + '"/>', None
    
enclitic = '''    <pardef n="enclitic">
      <!-- passthrough -->
      <e>
        <p>
          <l></l>
          <r></r>
        </p>
      </e>
      <!-- ই -->
      <e>
        <p>
          <l>ই</l>
          <r><j/>ই<s n="adv"/></r>
        </p>
      </e>
      <!-- ও -->
      <e>
        <p>
          <l>ও</l>
          <r><j/>ও<s n="adv"/></r>
        </p>
      </e>
    </pardef>'''

try:
    conn = MySQLdb.connect(host = 'localhost', user = 'root', passwd = 'root', db = 'bengali_conjugator')
    
    cursor = conn.cursor()
    cursor.execute('SET CHARACTER SET utf8')
	
    sql = ' SELECT lemma, animacy, gender FROM noun_source_freq '
    #sql = ' SELECT lemma, animacy, gender FROM noun_source_freq limit 15 '
    cursor.execute(sql)
	
    rows = cursor.fetchall()
    
    entries = {}
    
    for row in rows:
	db_lemma, db_animacy, db_gender = row
	#pprint(row)
	
	lemma = db_lemma
	gender = gender_table[db_gender]
	animacy = animacy_table[db_animacy]
	entries[lemma] = {'pos' : 'n', 'gender': gender, 'animacy': animacy, 'inflections': {}}
	
	#print lemma
	entries[lemma]['inflections']['nom'], entries[lemma]['inflections']['obj'], entries[lemma]['inflections']['gen'], entries[lemma]['inflections']['loc'] = get_inflection(lemma = lemma, animacy = animacy)
    
    #pprint(entries)
    
    print '<dictionary>';
    print '  <pardefs>';
    
    print enclitic
    
    for lemma, properties in entries.iteritems():
	#pprint(lemma)
	#pprint(properties)
	pos = properties['pos']
	gender = properties['gender']
	animacy = properties['animacy']
	print '    <pardef n="' + lemma + '__' + pos + '_' + gender +'">'     
        
	for case, details in properties['inflections'].iteritems():
	    #print case, details
	    for type, details2 in details.iteritems():
		#print case, type, details2
		if details2 == None:
		    continue
		for number, affix in details2.iteritems():
		    #print case, type, number, affix
		    print '      <e>'
		    print '        <p>'
		    print '          <l>' + affix + '</l>'
		    r = get_sym([pos, gender, animacy])
		    number_symbol, def_symbol = get_num(number)
		    r = r + number_symbol + get_sym([case])
		    if def_symbol != None:
			r = r + def_symbol
		    print '          <r>' + r +'</r>'
		    print '        </p>'
		    print '        <par n="enclitic"/>'
		    print '      </e>'
		    
		    # add enclitic e
		    
		    # add enclitic o
		    
	print '    </pardef>'
	    
    print '  </pardefs>';
    print '  <section id="main" type="standard">'
    for lemma, properties in entries.iteritems():
        print '    <e lm="' + lemma + '"><i>' + lemma.replace(' ', '<b/>') +'</i><par n="' + lemma + '__' + properties['pos'] + '_' + properties['gender'] + '"/></e>'
    print '  </section>'
    print '</dictionary>'
    
	
except MySQLdb.Error, e:
	print 'Error %d: %s' % (e.args[0], e.args[1])
	sys.exit (1)



