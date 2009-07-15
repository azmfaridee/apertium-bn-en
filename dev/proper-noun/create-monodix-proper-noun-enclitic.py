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


V = "[অআইঈউঊঋএঐওঔ]"
C = "[কখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়ঁ]"
K = "[ািীুূৃেৈোৌ]"

#'[অআইঈউঊঋএঐওঔ‌‌](ঁ)?', 'বই')
def get_inflection(stem, animate):
    nom = None
    obj = None
    gen = None
    loc = None
    stem = stem.strip()     
    
    # যমুনা
    pattern = 'া(ঁ)?$'
    if re.search(pattern, stem):
        #print 'yamuna'
        if animate == True:
            nom = stem
            obj = stem + 'কে'
            gen = stem + 'র'
            loc = None
        else:
            nom = stem
            obj = stem
            gen = stem + 'র'
            loc = stem + 'য়'
        return nom, obj, gen, loc       
    
    # রাজশাহী    
    pattern = K + '(ঁ)?$'
    if re.search(pattern, stem):
        #print 'yamuna'
        if animate == True:
            nom = stem
            obj = stem + 'কে'
            gen = stem + 'র'
            loc = None
        else:
            nom = stem
            obj = stem
            gen = stem + 'র'
            loc = stem + 'তে'
        return nom, obj, gen, loc
        
        
    # সুমন
    pattern = C + '(ঁ)?$'
    if re.search(pattern, stem):
        #print 'suman'
        if animate == True:
            nom = stem
            obj = stem + 'কে'
            gen = stem + 'ের'
            loc = None
        else:
            nom = stem
            obj = stem
            gen = stem + 'ের'
            loc = stem + 'ে'
        return nom, obj, gen, loc
        
    # কই
    pattern = V + '(ঁ)?$'
    if re.search(pattern, stem):
        #pdb.set_trace()
        #print 'Book'
        #print re.search(pattern, stem).group()
        if animate == True:
            nom = stem
            obj = stem + 'কে'
            gen = stem + 'য়ের'
            loc = None
        else:
            nom = stem
            obj = stem
            gen = stem + 'য়ের'
            loc = stem + 'য়ে'
        return nom, obj, gen, loc
    
#'[অআইঈউঊঋএঐওঔ‌‌](ঁ)?', 'বই')
def get_inflection2(stem, animate):
    nom = None
    obj = None
    gen = None
    loc = None
    stem = stem.strip()     
    
    # যমুনা
    pattern = 'া(ঁ)?$'
    if re.search(pattern, stem):
        #print 'yamuna'
        if animate == True:
            return '', 'কে', 'র', None
        else:
            return '', '', 'র', 'য়'
    
    # রাজশাহী    
    pattern = K + '(ঁ)?$'
    if re.search(pattern, stem):
        #print 'yamuna'
        if animate == True:
            return '', 'কে', 'র', None
        else:
            return '', '', 'র', 'তে'
        
    # সুমন
    pattern = C + '(ঁ)?$'
    if re.search(pattern, stem):
        #print 'suman'
        if animate == True:
            return '', 'কে', 'ের', None
        else:
            return '', '', 'ের', 'ে'
            
    # কই
    pattern = V + '(ঁ)?$'
    if re.search(pattern, stem):
        if animate == True:
            return '', 'কে', 'য়ের', None
        else:
            return '', '', 'য়ের', 'য়ে'

def get_symbols(list):
    symbols = []
    for e in list:
        s = ElementTree.Element('s', n = e)
        symbols.append(s)
    return symbols

def get_sym(list):
    sym = ''
    for e in list:
        sym = sym + '<s n=\"' + e + '\">'
    return sym

def get_enclitic_paradef():
    paradefs = []
    
    # ই
    paradef = ElementTree.Element('paradef', n = 'ই__enclitic')
    paradefs.append(paradef)
    e = ElementTree.Element('e')
    paradef.append(e)
    p = ElementTree.Element('p')
    e.append(p)
    p.append(ElementTree.Element('l'))
    r = ElementTree.Element('r')
    r.text = 'ই'
    r.append(ElementTree.Element('s', n = 'adv'))
    p.append(r)
    
    # ও
    paradef = ElementTree.Element('paradef', n = 'ও__enclitic')
    paradefs.append(paradef)
    e = ElementTree.Element('e')
    paradef.append(e)
    p = ElementTree.Element('p')
    e.append(p)
    p.append(ElementTree.Element('l'))
    r = ElementTree.Element('r')
    r.text = 'ও'
    r.append(ElementTree.Element('s', n = 'adv'))
    p.append(r)
    
    return paradefs
    
enclitic = """    <pardef n="ই__enclitic">
      <!-- passthrough -->
      <e>
        <p>
          <l></l>
          <r></r>
        </p>
      </e>
      <e>
        <p>
          <l>ই</l>
          <r><j/>ই<s n="adv"/></r>
        </p>
      </e>
    </pardef>
    <pardef n="ও__enclitic">
      <!-- passthrough -->
      <e>
        <p>
          <l></l>
          <r></r>
        </p>
      </e>
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
    #sql = " select lemma, gender, nptag from proper_noun_source_freq where nptag <> '6' and nptag = 0 limit 1"
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
        if nptag == '0':
            nom, obj, gen, loc = get_inflection2(lemma, True)
            # create enclitic
            nom_e, obj_e, gen_e, loc_e = nom + 'ই', obj + 'ই', gen + 'ই', None
            nom_o, obj_o, gen_o, loc_o = nom + 'ও', obj + 'ও', gen + 'ও', None   
        else:
            nom, obj, gen, loc = get_inflection2(lemma, False)
            # create enclitic
            nom_e, obj_e, gen_e, loc_e = nom + 'ই', obj + 'ই', gen + 'ই', loc + 'ই'
            nom_o, obj_o, gen_o, loc_o = nom + 'ও', obj + 'ও', gen + 'ও', loc + 'ও'
        
        dic_nom = {'surface': nom, 'number': 'sg', 'case': 'nom', 'enclitic': None}
        dic_nom_e = {'surface': nom_e, 'number': 'sg', 'case': 'nom', 'enclitic': enclitic_e}
        dic_nom_o = {'surface': nom_o, 'number': 'sg', 'case': 'nom', 'enclitic': enclitic_o}
        
        dic_obj = {'surface': obj, 'number': 'sg', 'case': 'obj', 'enclitic': None}
        dic_obj_e = {'surface': obj_e, 'number': 'sg', 'case': 'obj', 'enclitic': enclitic_e}
        dic_obj_o = {'surface': obj_o, 'number': 'sg', 'case': 'obj', 'enclitic': enclitic_o}
        
        dic_gen = {'surface': gen, 'number': 'sg', 'case': 'gen', 'enclitic': None}
        dic_gen_e = {'surface': gen_e, 'number': 'sg', 'case': 'gen', 'enclitic': enclitic_e}
        dic_gen_o = {'surface': gen_o, 'number': 'sg', 'case': 'gen', 'enclitic': enclitic_o}
                
        if loc != None:
            dic_loc = {'surface': loc, 'number': 'sg', 'case': 'loc', 'enclitic': None}
            dic_loc_e = {'surface': loc_e, 'number': 'sg', 'case': 'loc', 'enclitic': enclitic_e}
            dic_loc_o = {'surface': loc_o, 'number': 'sg', 'case': 'loc', 'enclitic': enclitic_o}        
        else:
            dic_loc = None
            dic_loc_e = None
            dic_loc_o = None
            
        entries[lemma] = {'pos' : 'np',
                          'subtype': nptype[nptag],
                          'gender': gendertype[gender],
                          'inflections': {'nom': dic_nom,
                                        'obj': dic_obj,
                                        'gen': dic_gen,
                                        'loc': dic_loc,
                                        
                                        'nom_e': dic_nom_e,
                                        'obj_e': dic_obj_e,
                                        'gen_e': dic_gen_e,
                                        'loc_e': dic_loc_e,
                                        
                                        'nom_o': dic_nom_o,
                                        'obj_o': dic_obj_o,
                                        'gen_o': dic_gen_o,
                                        'loc_o': dic_loc_o
                            }
                          }
    """
    dictionary = ElementTree.Element('dictionary')
    paradefs = ElementTree.Element('paradefs')
    dictionary.append(paradefs)

    section = ElementTree.Element('section', id="main", type="standard")
    dictionary.append(section)
    
    #enclitic paradefs
    for paradef in get_enclitic_paradef():
        paradefs.append(paradef)

    #pprint(entries)
    for lemma, properties in entries.iteritems():
        paradef = ElementTree.Element('paradef', n=lemma + '__' + properties['pos'] + '_' + properties['gender'])
        paradefs.append(paradef)
        for inflection, details in properties['inflections'].iteritems():
            if details == None:
                continue
            #print details
            e = ElementTree.Element('e')
            paradef.append(e)
            
            p = ElementTree.Element('p')
            e.append(p)
            
            l = ElementTree.Element('l')
            l.text = details['surface']
            p.append(l)
            
            r = ElementTree.Element('r')
            for s in get_symbols([properties['pos'], properties['gender'], properties['subtype'], details['number'], details['case']]):
                r.append(s)
            if details['enclitic']:
                r.append(ElementTree.Element('j'))
                r.append(ElementTree.Element('par', n = details['enclitic']['par']))
            p.append(r)
         
    #section
    for lemma, properties in entries.iteritems():
        e = ElementTree.Element('e', lm = lemma)
        section.append(e)
        
        i = ElementTree.Element('i')
        i.text = lemma.replace(' ', '###')
        e.append(i)
        
        par = ElementTree.Element('par', n=lemma + '__' + properties['pos'] + '_' + properties['gender'])
        e.append(par)
        
    # create the xml string
    string = ElementTree.tostring(dictionary, encoding='utf-8')
    doc = minidom.parseString(string)
    doc.normalize()
    string = doc.toprettyxml().replace('###', '<b/>')
    print string"""
    
    print '<dictionary>';
    print '  <pardefs>';
    
    print enclitic
    for lemma, properties in entries.iteritems():
        print '    <paradef n=\"' + lemma + '__' + properties['pos'] + '_' + properties['gender']+'\">'
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
            print '          <r>' + get_sym([properties['pos'], properties['gender'], properties['subtype'], details['number'], details['case']]) +'</r>'
            print '        </p>'
            if details['enclitic']:
                print '        <par n=\"' + details['enclitic']['par'] +'\">'
            print '      </e>'
        print '    </paradef>'
        
        """paradef = ElementTree.Element('paradef', n=lemma + '__' + properties['pos'] + '_' + properties['gender'])
        paradefs.append(paradef)
        for inflection, details in properties['inflections'].iteritems():
            if details == None:
                continue
            #print details
            e = ElementTree.Element('e')
            paradef.append(e)
            
            p = ElementTree.Element('p')
            e.append(p)
            
            l = ElementTree.Element('l')
            l.text = details['surface']
            p.append(l)
            
            r = ElementTree.Element('r')
            for s in get_symbols([properties['pos'], properties['gender'], properties['subtype'], details['number'], details['case']]):
                r.append(s)
            if details['enclitic']:
                r.append(ElementTree.Element('j'))
                r.append(ElementTree.Element('par', n = details['enclitic']['par']))
            p.append(r)"""
    
    print '  </pardefs>';
    print '  <section id="main" type="standard"/>';
    for lemma, properties in entries.iteritems():
        print '    <e lm=\"' + lemma + '\"><i>' + lemma.replace(' ', '<b/>') +'</i><par n=\"' + lemma + '__' + properties['pos'] + '_' + properties['gender'] + '\"/></e>'      
    print '  </section>';
    print '</dictionary>';

    
except MySQLdb.Error, e:
	print "Error %d: %s" % (e.args[0], e.args[1])
	sys.exit (1)
