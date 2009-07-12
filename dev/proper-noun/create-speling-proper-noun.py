#!/usr/bin/python2.5
# coding=utf-8
# -*- encoding: utf-8 -*-

import os
import sys
import MySQLdb
import re
import pdb

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
        

try:
    conn = MySQLdb.connect(host = "localhost", user = "root", passwd = "root", db = "bengali_conjugator")
    
    cursor = conn.cursor()
    cursor.execute('SET CHARACTER SET utf8')
	
    ''' Note: we are excluding type 6, this type now hold the errors that anubadok created '''
    sql = " select lemma, gender, nptag from proper_noun_source_freq where nptag <> '6' "
    cursor.execute(sql)
	
    rows = cursor.fetchall()
	
    gender_tag = None
    for row in rows: #{
        lemma, gender, nptag = row
        if nptag == '0': #{
        # we got a human name
            if gender == '1': #{
            # if male gender
                gender_tag = 'm'
            #}
            if gender == '2': #{
                gender_tag = 'f'
            #}
            nom, obj, gen, loc =  get_inflection(lemma, True)
            print lemma + "; " + nom + "; " + 'sg.nom' + "; " + "np." + gender_tag 
            print lemma + "; " + obj + "; " + 'sg.obj' + "; " + "np." + gender_tag
            print lemma + "; " + gen + "; " + 'sg.gen' + "; " + "np." + gender_tag 
        #}
        # we got some geological name
        if nptag == '1': #{
            nom, obj, gen, loc =  get_inflection(lemma, False)
            print lemma + "; " + nom + "; " + 'sg.nom' + "; np" 
            print lemma + "; " + obj + "; " + 'sg.obj' + "; np"
            print lemma + "; " + gen + "; " + 'sg.gen' + "; np"
            print lemma + "; " + loc + "; " + 'sg.loc' + "; np"
        #}
        # misc or org
        if nptag == '5' or nptag == '4': #{
            nom, obj, gen, loc =  get_inflection(lemma, False)
            print lemma + "; " + nom + "; " + 'sg.nom' + "; np" 
            print lemma + "; " + obj + "; " + 'sg.obj' + "; np"
            print lemma + "; " + gen + "; " + 'sg.gen' + "; np"
            print lemma + "; " + loc + "; " + 'sg.loc' + "; np"
        #}            
    #}

	
except MySQLdb.Error, e:
	print "Error %d: %s" % (e.args[0], e.args[1])
	sys.exit (1)



