#!/usr/bin/python2.5
# coding=utf-8
# -*- encoding: utf-8 -*-

''' This script writes noun speling format to stdout '''

import sys, string, codecs, MySQLdb;

#sys.stdin = codecs.getreader('utf-8')(sys.stdin);
#sys.stdout = codecs.getwriter('utf-8')(sys.stdout);
#sys.stderr = codecs.getwriter('utf-8')(sys.stderr);

try:
    conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "root", db = "bengali_conjugator")
    
    cursor = conn.cursor ()
    cursor.execute ('SET CHARACTER SET utf8')
    
    cursor.execute ("""SELECT lemma, inflection, animacy, gram_case, number, gender FROM noun_working_copy n""")
    
    rows = cursor.fetchall()
    
    for row in rows:
        stem, surface, animacy, gcase, number, gender = row
        if surface != '':
    	    sys.stdout.write(stem + "; " + surface + "; " + animacy + ".")
    	    if number == 'sd':
    	        sys.stdout.write('sg.')
            else:
                sys.stdout.write(number + '.')
    	    sys.stdout.write(gcase)
    	    if number == 'sd':
    	        sys.stdout.write('.def')
            sys.stdout.write('; n.' + gender)		
            sys.stdout.write("\n")
	
    cursor.close ()
    conn.close ()

except MySQLdb.Error, e:
	print "Error %d: %s" % (e.args[0], e.args[1])
	sys.exit (1)

