#!/bin/sh

# adverb speling
../speling-paradigms.py adverb.bn.speling > /tmp/adverb.bn.dix
../paradigm-chopper.py /tmp/adverb.bn.dix > adverb.bn.dix

lt-expand adverb.bn.dix > adverb.bn.expand
