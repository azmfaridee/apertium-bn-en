#!/usr/bin/python
# coding=utf-8
# -*- encoding: utf-8 -*-


# Program info:
# use this program to fix common speling errors in bengali text
# ড় is sometimes written as ড + nukta (unicode value 09bc), we want to
# represent this with one character
# same is true for ঢ় and য় and ৎ (at least at the word ending section)

# Input: stdin, each line contains one Bengali word
# Output: stdout, each line contains one fixed Bengali word

import sys, codecs

reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

words = []

# load the data from stdin from buffer, sometime direct processing creates some
# problems
for x in sys.stdin:
  words.append(x.strip())
  
for word in words:
  # decoding is important
  word = word.decode('utf-8')
  
  # replace ত্  at the end with ৎ
  if word[-2:] == u'\u09a4\u09cd':  word = word[:-2] + u'\u09ce'
  
  # replacement for ড়, ঢ় and য় which ara written with nukta
  word = word.replace(u'\u09a1\u09bc', u'\u09dc').replace(u'\u09a2\u09bc', u'\u09dd').replace(u'\u09af\u09bc', u'\u09df')
  
  # output
  print >> sys.stdout, word
