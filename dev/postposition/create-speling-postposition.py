#!/usr/bin/python2.5
# coding=utf-8
# -*- encoding: utf-8 -*-


'''
    Quick and dirty make of postposition speling file, sorry Fran to keep you waithing ...
'''

import sys, string, codecs, MySQLdb;


try:
	conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "root", db = "bengali_conjugator")

	cursor = conn.cursor ()
	cursor.execute ('SET CHARACTER SET utf8')

	cursor.execute ("SELECT word FROM meaning where pos like 'in' or pos like 'rp'")
	
	rows = cursor.fetchall()
	
	for row in rows:
		lemma, = row	
		sys.stdout.write(lemma + "; " + lemma + "; ; post\n")
	
	#some new adverbs, we need to have a seperate table for this, but right now this is what we have
	cursor.execute (""" SELECT word from unknown_words where pos like '%7%' """)
	
	rows = cursor.fetchall()
	
	for row in rows:
		word, = row	
		sys.stdout.write(word + "; " + word + "; ; post\n")
	
	
	cursor.close ()
	conn.close ()

except MySQLdb.Error, e:
	print "Error %d: %s" % (e.args[0], e.args[1])
	sys.exit (1)

