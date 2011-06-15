#!/bin/bash

cat adjective.bn.dix | grep "<e lm" | perl -pe "s/( )*<e.*n=\"//g" | perl -pe 's/__.*//g' | python ../../../uniq.py > /tmp/foo

cat adj.pardefs | sed 's/,.*//g' > /tmp/foo1

cat /tmp/foo | grep -v -w -f /tmp/foo1 | sed 's/$/,-1/g' | cat >> adj.pardefs
