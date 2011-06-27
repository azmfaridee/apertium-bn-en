#!/bin/bash

cat adv.pardefs | grep -v "^$" | sed 's/,/\t/g' | cut -f1 | sed 's/^/<i>/g' | sed 's/$/<\/i>/g' > /tmp/foo
cat adverb.bn.dix | sed 's/.*e lm.*//g' | grep -v "^$" > /tmp/foo1
cat adverb.bn.dix | grep "e lm" | grep -w -f /tmp/foo > /tmp/foo2
cat /tmp/foo1 | head -n-2 > /tmp/foo3
cat /tmp/foo1 | tail -2 > /tmp/foo4
cat /tmp/foo2 | cat >> /tmp/foo3
cat /tmp/foo4 | cat >> /tmp/foo3
lt-expand /tmp/foo3 > adv.inflections
