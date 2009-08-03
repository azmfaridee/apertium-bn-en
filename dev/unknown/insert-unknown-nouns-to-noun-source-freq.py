#!/usr/bin/python2.5
# coding=utf-8
# -*- encoding: utf-8 -*-

import os
import sys
import MySQLdb
import re
import pdb

''' we use this script to insert new unknown words into our database '''

        
try:    
    # create the connection
    conn = MySQLdb.connect(host = "localhost", user = "root", passwd = "root", db = "bengali_conjugator")
    
    cursor = conn.cursor()
    cursor.execute('SET CHARACTER SET utf8')
	
    sql = ''' SELECT word FROM unknown_words where pos like '%0%' and pos not like '%10%' '''
    cursor.execute(sql)    	
    rows = cursor.fetchall()
    
    for row in rows:
        word, = row
        #print word
        
        # we need to check if this word already exists in the noun table
        sql_check = ''' SELECT count(*) as n FROM noun_source_freq where lemma = '%(word)s' ''' % {'word': word}
        cursor.execute(sql_check)
        n, = cursor.fetchone()
        if n == 0:
            print 'Inserting ' + word
            sql_insert = ''' insert into noun_source_freq(lemma, animacy, freq, gender, old) values('%(word)s', 0, 0, 0, 0) ''' % {'word': word}     
            cursor.execute(sql_insert)
        
except MySQLdb.Error, e:
	print "Error %d: %s" % (e.args[0], e.args[1])
	sys.exit (1)

