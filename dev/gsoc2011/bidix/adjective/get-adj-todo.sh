#!/bin/bash

#	gets the next adjectives those needs entries to bidix by following :
#		> expand adjectives from monodix
#		> collect all the entries from adj.ambiguous, adj.todo, adj.patch
#		> subtract from the expanded list
#		> append new entries to adj.todo

lt-expand ../../../../apertium-bn-en.bn.dix| grep '<adj>' | sed 's/:>:/:/g' | sed 's/:<:/:/g' | cut -f2 -d':' | perl -pe 's/<comp>|<sup>//g' | python ../../../uniq.py | tee /tmp/adjtot1 | perl -pe 's/(<).*//g' > /tmp/adjtot
cat adj.patch | egrep -v "\!" | sed 's/ //g' | sed 's/^/\^/g' | grep -v "\^$" | perl -pe 's/\^//g' | perl -pe 's/<e.*<l>//g' | perl -pe 's/(<).*//g' | python ../../../uniq.py > /tmp/adjexis
cat adj.ambiguous | perl -pe 's/(<).*//g' | cat >> /tmp/adjexis
cat adj.todo | perl -pe 's/(<).*//g' | cat >> /tmp/adjexis

noe_=`grep -c '' adj.todo`

cat /tmp/adjexis | grep -v '^$' > /tmp/adjexis1
cat /tmp/adjtot | grep -v -w -f /tmp/adjexis1 > /tmp/bar6
cat /tmp/adjtot1 | sed 's/<adj>/ <adj>/g' | grep -w -f /tmp/bar6 | sed 's/ //g' | sed 's/$/\t\!/g' | cat >> adj.todo

noe=`grep -c '' adj.todo`
noe=`expr $noe - $noe_`
echo "$noe entries added to todo list"   
