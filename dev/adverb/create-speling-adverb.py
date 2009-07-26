#!/usr/bin/python2.5
# coding=utf-8
# -*- encoding: utf-8 -*-


'''
    TODO: proper handle for preadv and cnjadv
'''

import sys, string, codecs, MySQLdb;


try:
	conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "root", db = "bengali_conjugator")

	cursor = conn.cursor ()
	cursor.execute ('SET CHARACTER SET utf8')

	cursor.execute ("select word from meaning where pos like 'RB'")
	
	rows = cursor.fetchall()
	
	for row in rows:
		lemma, = row	
		sys.stdout.write(lemma + "; " + lemma + "; ;adv\n")
	
	#some new adverbs, we need to have a seperate table for this, but right now this is what we have
	cursor.execute (""" SELECT word from unknown_words where pos like '%4%' """)
	
	rows = cursor.fetchall()
	
	for row in rows:
		word, = row	
		sys.stdout.write(word + "; " + word + ";;adv\n")
	
	cursor.close ()
	conn.close ()
	
except MySQLdb.Error, e:
	print "Error %d: %s" % (e.args[0], e.args[1])
	sys.exit (1)

