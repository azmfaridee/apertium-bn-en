#!/bin/sh

# postposition speling
#../speling-paradigms.py postposition.bn.speling > /tmp/postposition.bn.dix
#../paradigm-chopper.py /tmp/postposition.bn.dix > postposition.bn.dix

# update speling from the list file, if you have new postpositions, just append them to this list
cat ./postposition.bn.list | awk '{ print $0"; "$0"; ;post" }' > ./postposition.bn.speling

# this solves the "" bug for now
./to-dix-quick.sh postposition.bn.speling > postposition.bn.dix
