#!/bin/sh

# noun speling
#../speling-paradigms.py noun.bn.speling > /tmp/noun.bn.dix

# we have a separate script for adding enclitic, speling file will not work here
./create-monodix-noun-enclitic.py > /tmp/noun.bn.dix
../paradigm-chopper.py /tmp/noun.bn.dix > noun.bn.dix

#./create-monodix-noun-enclitic.py > noun.bn.dix

# expand
lt-expand noun.bn.dix > noun.bn.expand

