#!/bin/bash

# with the monodix entries for proper-noun in 'proper-noun.bn.dix' this script generates
# the uniqe pardefs used in 'proper-noun' and dumps to 'proper-noun.pardefs

cat proper-noun.bn.dix | grep "<e lm" | perl -pe "s/( )*<e.*n=\"//g" | perl -pe 's/__.*//g' | python ../../../uniq.py > proper-noun.pardefs
