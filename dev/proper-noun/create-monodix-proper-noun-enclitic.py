#!/usr/bin/python2.6
# coding=utf-8
# -*- encoding: utf-8 -*-

import os
import string
import sys
import codecs
import re
import MySQLdb
import pdb
from xml.etree import ElementTree
from xml.dom import minidom
from pprint import pprint

sys.stdin = codecs.getreader('utf-8')(sys.stdin);
sys.stdout = codecs.getwriter('utf-8')(sys.stdout);
sys.stderr = codecs.getwriter('utf-8')(sys.stderr);

BnChars = {'vowel': u'[অআইঈউঊঋএঐওঔ]',
	   'consonant_real': u'[কখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহৎড়ঢ়য়]',
	   'marker': u'[ািীুূৃেৈোৌ]',
	   'number': u'[০১২৩৪৫৬৭৮৯]',
	   'misc': u'[ঁংঃ]',
	   
	   'hasant': u'[্]',
	   'anusvara': u'[ং]',
	   'chandrabindu': u'[ঁ]',
	   'visarga': u'[ঃ]',
	   
	   'consonant': u'[কখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহৎড়ঢ়য়' + u'ংঃ' + u'্]'}
   
#'[অআইঈউঊঋএঐওঔ‌‌](ঁ)?', 'বই')
def get_inflection2(stem, animate):
    # be careful this is needed
    stem = stem.strip().decode('utf-8')
    
    # যমুনা
    regex = u'া(ঁ)?$'
    pattern = re.compile(regex)
    if pattern.search(stem):
        #print 'yamuna'
        if animate == True:
            return u'', u'কে', u'র', None
        else:
            return u'', u'', 'র', u'য়'
    
    # রাজশাহী    
    regex = BnChars['marker'] + u'(ঁ)?$'
    pattern = re.compile(regex)
    if pattern.search(stem):
        #print 'rajshahi'
        if animate == True:
            return '', 'কে', 'র', None
        else:
            return '', '', 'র', 'তে'
        
    # সুমন
    regex = BnChars['consonant'] + u'$'
    pattern = re.compile(regex)
    if pattern.search(stem):
        #print 'suman'
        if animate == True:
            return '', 'কে', 'ের', None
        else:
            return '', '', 'ের', 'ে'
            
    # কই
    regex = BnChars['vowel'] + u'(ঁ)?$'
    pattern = re.compile(regex)
    if pattern.search(stem):
        #print 'koi'
        if animate == True:
            return '', 'কে', 'য়ের', None
        else:
            return '', '', 'য়ের', 'য়ে'
    
    print 'Nothing'

def get_sym(list):
    sym = ''
    for e in list:
        sym = sym + '<s n=\"' + e + '\"/>'
    return sym

enclitic = """    <pardef n="enclitic">
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
    </pardef>"""
    
try:
    conn = MySQLdb.connect(host = "localhost", user = "root", passwd = "root", db = "bengali_conjugator")
    
    cursor = conn.cursor()
    cursor.execute('SET CHARACTER SET utf8')
	
    ''' Note: we are excluding type 6, this type now hold the errors that anubadok created '''
    #sql = " select lemma, gender, nptag from proper_noun_source_freq where nptag <> '6' and nptag = 0 limit 30"
    sql = " select lemma, gender, nptag from proper_noun_source_freq where nptag <> '6'"
    cursor.execute(sql)
	
    rows = cursor.fetchall()
    
    entries = {}
    nptype = {'0': 'ant', '1': 'top', '2': 'hyd', '3': 'cog', '4': 'org', '5': 'al'}
    gendertype = {'0': 'mf', '1': 'm', '2': 'f'}
    enclitic_e = {'par': 'ই__enclitic', 'pos': 'adv'}
    enclitic_o = {'par': 'ও__enclitic', 'pos': 'adv'}
    	
    for row in rows:
        lemma, gender, nptag = row
        #print 'DEBUG ' + lemma
        if nptag == '0':
            nom, obj, gen, loc = get_inflection2(lemma, True)
        else:
            nom, obj, gen, loc = get_inflection2(lemma, False)
        
        dic_nom = {'surface': nom, 'number': 'sg', 'case': 'nom', 'enclitic': None}
        
        dic_obj = {'surface': obj, 'number': 'sg', 'case': 'obj', 'enclitic': None}
        
        dic_gen = {'surface': gen, 'number': 'sg', 'case': 'gen', 'enclitic': None}
                
        if loc != None:
            dic_loc = {'surface': loc, 'number': 'sg', 'case': 'loc', 'enclitic': None}
        else:
            dic_loc = None
            
        entries[lemma] = {'pos' : 'np',
                          'subtype': nptype[nptag],
                          'gender': gendertype[gender],
                          'inflections': {'nom': dic_nom,
                                        'obj': dic_obj,
                                        'gen': dic_gen,
                                        'loc': dic_loc
                            }
                          }
        
        
    #pprint(entries)
    
    print '<dictionary>';
    print '  <pardefs>';
    
    print enclitic
    for lemma, properties in entries.iteritems():
        print '    <pardef n=\"' + lemma + '__' + properties['pos'] + '_' + properties['gender']+'\">'
        for inflection, details in properties['inflections'].iteritems():
            if details == None:
                continue
            print '      <e>'
            print '        <p>'
            '''
            # this snipped removes the enclitic from the l part so that it can be passed to its enclitic paradef, is this really necessary?
            if details['enclitic']:
                l = details['surface'].decode('utf-8')[:details['surface'].rfind(details['enclitic']['par'].decode('utf-8')[:1])]
            else:
                l = details['surface']'''
            l = details['surface']
            print '          <l>' + l + '</l>'
            print '          <r>' + get_sym([properties['pos'], properties['subtype'], properties['gender'], details['number'], details['case']]) +'</r>'
            print '        </p>'
            '''if details['enclitic']:
                print '        <par n=\"' + details['enclitic']['par'] +'\"/>'
            '''
            print '        <par n=\"enclitic\"/>'
            print '      </e>'
        print '    </pardef>'
    
    print '  </pardefs>';
    print '  <section id="main" type="standard">';
    for lemma, properties in entries.iteritems():
        print '    <e lm=\"' + lemma + '\"><i>' + lemma.replace(' ', '<b/>') +'</i><par n=\"' + lemma + '__' + properties['pos'] + '_' + properties['gender'] + '\"/></e>'      
    print '  </section>';
    print '</dictionary>';

    
except MySQLdb.Error, e:
	print "Error %d: %s" % (e.args[0], e.args[1])
	sys.exit (1)
