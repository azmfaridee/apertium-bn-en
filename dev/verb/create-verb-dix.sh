#!/bin/sh

# verb speling
./create-monodix-verb-enclitic.py > /tmp/verb.bn.dix
../paradigm-chopper.py /tmp/verb.bn.dix > verb.bn.dix

lt-expand verb.bn.dix > verb.bn.expand

