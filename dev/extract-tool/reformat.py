#!/usr/bin/python
# coding=utf-8
# -*- encoding: utf-8 -*-

import sys, re

# regex for the paradefs
regex_par = '(paradigm )([ঁংঃঅআইঈউঊঋঌএঐওঔকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহ়ঽািীুূৃৄেৈোৌ্ৎৗড়ঢ়য়ৠৡৢৣ০১২৩৪৫৬৭৮৯ৰৱ৲৳৴৵৶৷৸৹৺/]+)(__)'
regex_par_name = '[ঁংঃঅআইঈউঊঋঌএঐওঔকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহ়ঽািীুূৃৄেৈোৌ্ৎৗড়ঢ়য়ৠৡৢৣ০১২৩৪৫৬৭৮৯ৰৱ৲৳৴৵৶৷৸৹৺/]+'

# global variable to for the dummy paradef names
index = 0

# generate dummy paradef 
def gen_par():
    global index
    parname = 'par' + str(index)
    index =  index + 1
    return parname

# argument check
## if len(sys.argv) < 2:
##     print 'Provide a source file'
##     exit(1)

## doc = open(sys.argv[1])
## doc = open('apertium-bn-en.bn.extract')

doc = sys.stdin

for line in doc:
    # replace the newlines
    line = line.replace('\n','')
    # match agains the ragex
    match = re.search(regex_par, line)
    if match:
        # we got the paradef line, replace the bengali paradef name with a generated par
        par_name = re.search(regex_par_name, match.group()).group()
        print line.replace(par_name, gen_par())
    else:
        # print the other line normally
        print line
