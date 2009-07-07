#!/usr/bin/python2.5
# coding=utf-8
# -*- encoding: utf-8 -*-

''' this script processes the unknown word list from apertium format'''
import os
import sys
import re

alpha = '১২৩৪৫৬৭৮৯০অআইঈউঊঋএঐওঔকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়ঁািীুূৃেৈোৌংঃ্'
word = '[' + alpha + ']+'
regex = '(\^)(' + word + ')(\/\*)(' + word + ')(\$)'
p = re.compile(regex)
words = []

file = open('unknown.txt')
for line in file:
    words.append(p.search(line).group(2))
file.close()

for word in words:
    print word
