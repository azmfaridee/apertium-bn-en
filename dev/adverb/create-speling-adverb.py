#!/usr/bin/python2.5
# coding=utf-8
# -*- encoding: utf-8 -*-

import sys, string, codecs, MySQLdb;


try:
	conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "root", db = "bengali_conjugator")

	cursor = conn.cursor ()
	cursor.execute ('SET CHARACTER SET utf8')

	cursor.execute ("select word from meaning where pos like 'RB'")
	
	rows = cursor.fetchall()
	
	for row in rows:
		lemma, = row	
		sys.stdout.write(lemma + "; " + lemma + "; adv\n")
	
	cursor.close ()
	conn.close ()

except MySQLdb.Error, e:
	print "Error %d: %s" % (e.args[0], e.args[1])
	sys.exit (1)

