#!/bin/sh

# numeral speling
cat numerals.bn.list | awk -f create-numerals-speling.awk > numerals.bn.speling

../speling-paradigms.py numerals.bn.speling > /tmp/numerals.bn.dix
../paradigm-chopper.py /tmp/numerals.bn.dix > numerals.bn.dix

#../speling-paradigms.py numerals.bn.speling > numerals.bn.dix

lt-expand numerals.bn.dix > numerals.bn.expand


