#!/bin/sh

# postposition speling
#../speling-paradigms.py postposition.bn.speling > /tmp/postposition.bn.dix
#../paradigm-chopper.py /tmp/postposition.bn.dix > postposition.bn.dix

# this solves the "" bug for now
./to-dix-quick.sh postposition.bn.speling > postposition.bn.dix
