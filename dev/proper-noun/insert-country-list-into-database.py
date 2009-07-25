#!/usr/bin/python2.5
# coding=utf-8
# -*- encoding: utf-8 -*-

import os
import sys
import MySQLdb

class DBConnection:
    def __init__(self):
        self.conn = MySQLdb.connect(host = "localhost", user = "root", passwd = "root", db = "bengali_conjugator")
        self.cursor = self.conn.cursor()
        self.cursor.execute('SET CHARACTER SET utf8')
    
    def getcursor(self):
        return self.cursor
    
    def __del__(self):
        self.cursor.close()
        self.conn.close()

try:
    conn = DBConnection()
    cursor = conn.getcursor()
    
    country_list = open('country-list')
    for country in country_list:
	country = country.strip()
        sql_chek = ''' SELECT count(*) FROM proper_noun_source_freq where lemma = '%s' ''' % country
        #print >> sys.stderr, sql_chek
        cursor.execute(sql_chek)
        n, = cursor.fetchone()
        if n == 0:
            sql_insert = ''' insert into proper_noun_source_freq(lemma, animacy, freq, gender, number, nptag) values('%s', '0', '0', '0', '0', '1') ''' % country
	    print >> sys.stderr, sql_insert
            cursor.execute(sql_insert)
        
    
    country_list.close()
    
except MySQLdb.Error, e:
	print "Error %d: %s" % (e.args[0], e.args[1])
	sys.exit (1)



