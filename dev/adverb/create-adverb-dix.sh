#!/bin/sh

# adverb speling, we are not using this right now
#../speling-paradigms.py adverb.bn.speling > /tmp/adverb.bn.dix
#../paradigm-chopper.py /tmp/adverb.bn.dix > adverb.bn.dix

./to-dix-quick.sh adverb.bn.speling > adverb.bn.dix

lt-expand adverb.bn.dix > adverb.bn.expand
