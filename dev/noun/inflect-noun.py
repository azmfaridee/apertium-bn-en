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
    # just for safety
    stem = stem.strip()
    animate = animate.strip()    
        
        # যমুনা
    regex = K + '(ঁ)?$'
    if re.search(regex, stem):
        #print 'yamuna'
        if animate == True:
            nom = stem, stem + 'টা' ,  stem + 'রা'
            obj = stem + 'কে',  stem + 'টাকে' ,  stem + 'দেরকে'
            gen = stem + 'র',  stem + 'টার' ,  stem + 'দের'
            loc = None
        else:
            nom = stem, stem + 'টা' ,  stem + 'গুলো'
            obj = stem,  stem + 'টা' ,  stem + 'গুলো'
            gen = stem + 'র',  stem + 'টার' ,  stem + 'গুলোর'
            loc = stem + 'য়',  stem + 'টায়' ,  stem + 'গুলোয়'            
        return nom, obj, gen, loc
        
        
        # সুমন
    regex = C + '(ঁ)?$'
    if re.search(regex, stem):
        #print 'suman'
        if animate == True:
            nom = stem, stem + 'টা' ,  stem + 'েরা'
            obj = stem + 'কে',  stem + 'টাকে' ,  stem + 'দেরকে'
            gen = stem + 'ের',  stem + 'টার' ,  stem + 'দের'
            loc = None
        else:
            nom = stem, stem + 'টা' ,  stem + 'গুলো'
            obj = stem,  stem + 'টা' ,  stem + 'গুলো'
            gen = stem + 'ের',  stem + 'টার' ,  stem + 'গুলোর'
            loc = stem + 'ে',  stem + 'টায়' ,  stem + 'গুলোয়'
        return nom, obj, gen, loc
        
        # কই
    regex = V + '(ঁ)?$'
    if re.search(regex, stem):
        #pdb.set_trace()
        #print 'Book'
        #print re.search(regex, stem).group()
        if animate == True:
            nom = stem, stem + 'টা' ,  stem + 'য়েরা'
            obj = stem + 'কে',  stem + 'টাকে' ,  stem + 'দেরকে'
            gen = stem + 'য়ের',  stem + 'টার' ,  stem + 'দের'
            loc = None
        else:
            nom = stem, stem + 'টা' ,  stem + 'গুলো'
            obj = stem,  stem + 'টা' ,  stem + 'গুলো'
            gen = stem + 'য়ের',  stem + 'টার' ,  stem + 'গুলোর'
            loc = stem + 'য়ে',  stem + 'টায়' ,  stem + 'গুলোয়'
        return nom, obj, gen, loc
        

try:
    conn = MySQLdb.connect(host = "localhost", user = "root", passwd = "root", db = "bengali_conjugator")
    
    cursor = conn.cursor()
    cursor.execute('SET CHARACTER SET utf8')
	
    sql = " SELECT lemma, animacy, gender FROM noun_source_freq "
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
            print lemma + "; " + nom + "; " + 'sg.nom' + "; " + gender_tag + ".n" 
            print lemma + "; " + obj + "; " + 'sg.obj' + "; " + gender_tag + ".n"
            print lemma + "; " + gen + "; " + 'sg.gen' + "; " + gender_tag + ".n" 
        #}
        # we got some geological name
        if nptag == '1': #{
            nom, obj, gen, loc =  get_inflection(lemma, False)
            print lemma + "; " + nom + "; " + 'sg.nom' + "; n" 
            print lemma + "; " + obj + "; " + 'sg.obj' + "; n"
            print lemma + "; " + gen + "; " + 'sg.gen' + "; n"
            print lemma + "; " + loc + "; " + 'sg.loc' + "; n"
        #}
        # misc
        if nptag == '5': #{
            nom, obj, gen, loc =  get_inflection(lemma, False)
            print lemma + "; " + nom + "; " + 'sg.nom' + "; n" 
            print lemma + "; " + obj + "; " + 'sg.obj' + "; n"
            print lemma + "; " + gen + "; " + 'sg.gen' + "; n"
            print lemma + "; " + loc + "; " + 'sg.loc' + "; n"
        #}            
    #}

	
except MySQLdb.Error, e:
	print "Error %d: %s" % (e.args[0], e.args[1])
	sys.exit (1)



