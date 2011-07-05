#!/bin/bash

# with the monodix entries for adv in 'adverb.bn.dix' this script generates
# the uniqe pardefs used in 'adv' and dumps to 'adv.pardefs

cat adverb.bn.dix | grep "<e lm" | perl -pe "s/( )*<e.*n=\"//g" | perl -pe 's/__.*//g' | python ../../../uniq.py > adv.pardefs
