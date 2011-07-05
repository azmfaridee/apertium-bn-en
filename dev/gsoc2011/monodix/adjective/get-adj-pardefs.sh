#!/bin/bash

# with the monodix entries for adj in 'adjective.bn.dix' this script generates
# the uniqe pardefs used in 'adj' and dumps to 'adj.pardefs

cat adjective.bn.dix | grep "<e lm" | perl -pe "s/( )*<e.*n=\"//g" | perl -pe 's/__.*//g' | python ../../../uniq.py > /tmp/foo
