#!/bin/sh

# adverb speling, we are not using this right now
#../speling-paradigms.py adverb.bn.speling > /tmp/adverb.bn.dix
#../paradigm-chopper.py /tmp/adverb.bn.dix > adverb.bn.dix

# create speling from the list file, not the database
# run the prune script the remove the duplicates
cat adverb-extra.bn.list adverb-main.bn.list | ../prune.py > adverb.bn.list
cat ./adverb.bn.list | awk '{print $0"; "$0"; ;adv"}' > ./adverb.bn.speling

# quick dix
./to-dix-quick.sh adverb.bn.speling > adverb.bn.dix

lt-expand adverb.bn.dix > adverb.bn.expand
