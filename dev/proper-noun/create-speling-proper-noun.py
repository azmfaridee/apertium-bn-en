#!/usr/bin/python2.5
# coding=utf-8
# -*- encoding: utf-8 -*-

import os
import sys
import MySQLdb

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
        #}
        elif nptag == '1':
            pass
        else:
            pass
    #}

	
except MySQLdb.Error, e:
	print "Error %d: %s" % (e.args[0], e.args[1])
	sys.exit (1)



