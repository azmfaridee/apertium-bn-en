#!/usr/bin/python2.6
# coding=utf-8
# -*- encoding: utf-8 -*-

''' This script reads lines from stdin, finds the unique entries, sorts them and prints them '''
import sys
import os

entries = []
for line in sys.stdin:
    if line.strip() not in entries:
        entries.append(line.strip())

entries.sort()        
for line in entries:
    sys.stdout.write(line + '\n')