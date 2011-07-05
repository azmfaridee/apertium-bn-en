#!/bin/bash

# with the noun pardefs provided in 'adj.pardefs' and the 'adj.bn.dix' this script generates
# the root inflections for noun and dumps to 'adj.inflections'

cat adj.pardefs | grep -v "^$" | sed 's/,/\t/g' | cut -f1 | sed 's/^/<i>/g' | sed 's/$/<\/i>/g' > /tmp/foo
cat adjective.bn.dix | sed 's/.*e lm.*//g' | grep -v "^$" > /tmp/foo1
cat adjective.bn.dix | grep "e lm" | grep -w -f /tmp/foo > /tmp/foo2
cat /tmp/foo1 | head -n-2 > /tmp/foo3
cat /tmp/foo1 | tail -2 > /tmp/foo4
cat /tmp/foo2 | cat >> /tmp/foo3
cat /tmp/foo4 | cat >> /tmp/foo3
lt-expand /tmp/foo3 > adj.inflections
