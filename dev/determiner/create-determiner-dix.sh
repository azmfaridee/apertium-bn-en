#!/bin/sh

# determiner speling
./create-determiner-speling.sh > determiner.bn.speling
# there is some problem with determiner, we cannot use the chopper now :(

../speling-paradigms.py determiner.bn.speling > /tmp/determiner.bn.dix
../paradigm-chopper.py /tmp/determiner.bn.dix > determiner.bn.dix

#../speling-paradigms.py determiner.bn.speling > determiner.bn.dix

lt-expand determiner.bn.dix > determiner.bn.expand


