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
    # read the file
    lines = []      
    file = open('unknown-edited.list')
    for line in file:
        lines.append(line.strip())
    file.close()    
    
    # create the connection
    conn = MySQLdb.connect(host = "localhost", user = "root", passwd = "root", db = "bengali_conjugator")
    
    cursor = conn.cursor()
    cursor.execute('SET CHARACTER SET utf8')
	
    sql = " SELECT word, pos FROM unknown_words "
    cursor.execute(sql)    	
    rows = cursor.fetchall()
    
    
    for line in lines:
        found = False
        sql = " SELECT word, pos FROM unknown_words "
        cursor.execute(sql)    	
        rows = cursor.fetchall()
        for row in rows:
            word, pos = row
            if line == word:
                found = True
                break
        if found == True:
            print 'Found, not inserting ...'
        else:
            print 'Not Found, inserting ...'    
            sql_insert = """insert into unknown_words(word, pos) values('%(word)s', '')""" % {'word': line}
            cursor.execute(sql_insert)

	
except MySQLdb.Error, e:
	print "Error %d: %s" % (e.args[0], e.args[1])
	sys.exit (1)

