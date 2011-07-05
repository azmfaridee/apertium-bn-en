#!/bin/bash

# with the monodix entries for noun in 'noun.bn.dix' this script generates
# the uniqe pardefs used in 'noun' and dumps to 'noun.pardefs'

cat noun.bn.dix | grep "<e lm" | perl -pe "s/( )*<e.*n=\"//g" | perl -pe 's/__.*//g' | python ../../../uniq.py > noun.pardefs
