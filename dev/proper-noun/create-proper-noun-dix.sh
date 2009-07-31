#!/bin/sh

# proper-noun speling
./create-monodix-proper-noun-enclitic.py > /tmp/proper-noun.bn.dix
../paradigm-chopper.py /tmp/proper-noun.bn.dix > proper-noun.bn.dix

lt-expand proper-noun.bn.dix > proper-noun.bn.expand

