#!/usr/bin/python2.5
# coding=utf-8
# -*- encoding: utf-8 -*-

import sys

import MySQLdb

#sys.stdin = codecs.getreader('utf-8')(sys.stdin);
#sys.stdout = codecs.getwriter('utf-8')(sys.stdout);
#sys.stderr = codecs.getwriter('utf-8')(sys.stderr);

def get_sansktrit_inflection(lemma):
    ''' if ends with ৎ, then replace with ত '''
    if lemma[-1] =='ৎ':
        lemma[-1] = 'ত'
    ''' if ends with TA, then add a HASHANT otherwise do as normal '''
    if lemma[-1] == 'ত':
        comp = lemma + '্তর'
        sup = lemma + '্তম'
    else:
        comp = lemma + 'তর'
        sup = lemma + 'তম'
	return comp, sup

def get_normal_inflection(lemma):
	comp = 'অপেক্ষাকৃত ' + lemma
	sup = 'সবচাইতে ' + lemma
	return comp, sup

class Connection(object):
    def __init__(self):
        pass
    def __del__(self):
        pass

try:
    #conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "root", db = "bengali_conjugator", use_unicode = True)
    conn = MySQLdb.connect (host="localhost", user="root", passwd="root", db="bengali_conjugator")

    cursor = conn.cursor ()

    cursor.execute ('SET CHARACTER SET utf8')

    query = ''' SELECT lemma, has_degree, gender FROM adj_freq a '''
    cursor.execute (query)
    rows = cursor.fetchall()
    for row in rows:
        lemma, degree, gender = row
#        print lemma, degree, gender

        gendertag = {'0': 'mf', '1': 'm', '2': 'f'}
        gender = gendertag[gender]

        # when the adjective has no inflection
        if(degree == '0'):
            sys.stdout.write(lemma + "; " + lemma + "; " + gender + "; adj\n")
        # when the adjective is fully synthetic
        if(degree == '1'):
            comp, sup = get_sansktrit_inflection(lemma)
            sys.stdout.write(lemma + "; " + lemma + "; sint." + gender + "; adj\n")
            sys.stdout.write(lemma + "; " + comp + "; " + "sint.comp." + gender + "; adj\n")
            sys.stdout.write(lemma + "; " + sup + "; " + "sint.sup." + gender + "; adj\n")
        # when the adjective has only synth superlative
        if(degree == '2'):
            comp, sup = get_sansktrit_inflection(lemma)
            sys.stdout.write(lemma + "; " + lemma + "; psint." + gender + "; adj\n")
            sys.stdout.write(lemma + "; " + sup + "; " + "psint.sup." + gender + "; adj\n")
        # when the adjective has only syth comparative, no superlative
        if(degree == '3'):
            comp, sup = get_sansktrit_inflection(lemma)
            sys.stdout.write(lemma + "; " + lemma + "; psint." + gender + "; adj\n")
            sys.stdout.write(lemma + "; " + comp + "; " + "psint.comp." + gender + "; adj\n")
    cursor.close ()
    conn.close ()

except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit (1)
