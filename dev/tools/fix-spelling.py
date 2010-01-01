#!/usr/bin/python

import sys, codecs

words = []
for x in sys.stdin: words.append(x.strip())
for index, value in enumerate(words):
  word = words[index].decode('utf-8')
  # replace ত্  at the end with ৎ
  if word[-2:] == u'\u09a4\u09cd':  word = word[:-2] + u'\u09ce'
  # replacement for ড়, ঢ় and য় which ara written with nukta
  word = word.replace(u'\u09a1\u09bc', u'\u09dc').replace(u'\u09a2\u09bc', u'\u09dd').replace(u'\u09af\u09bc', u'\u09df')
  print >> sys.stdout, word
