#!/bin/bash

#	gets the next nouns those needs entries to bidix by following :
#		> expand nouns from monodix
#		> collect all the entries from noun.ambiguous, noun.todo, noun.patch
#		> subtract from the expanded list
#		> append new entries to noun.todo

lt-expand ../../../../apertium-bn-en.bn.dix| grep '<n>' | sed 's/:>:/:/g' | sed 's/:<:/:/g' | cut -f2 -d':' | perl -pe 's/(<sg>|<pl>).*//g' | python ../../../uniq.py | tee /tmp/nountot1 | perl -pe 's/(<).*//g' > /tmp/nountot
cat noun.patch | egrep -v "\!" | sed 's/ //g' | sed 's/^/\^/g' | grep -v "\^$" | perl -pe 's/\^//g' | perl -pe 's/<e.*<l>//g' | perl -pe 's/(<).*//g' | python ../../../uniq.py > /tmp/nounexis
cat noun.ambiguous | perl -pe 's/(<).*//g' | cat >> /tmp/nounexis
cat noun.todo | perl -pe 's/(<).*//g' | cat >> /tmp/nounexis

noe_=`grep -c '' noun.todo`

cat /tmp/nounexis | grep -v '^$' > /tmp/nounexis1
cat /tmp/nountot | grep -v -w -f /tmp/nounexis1 > /tmp/bar6
cat /tmp/nountot1 | sed 's/<n>/ <n>/g' | grep -w -f /tmp/bar6 | sed 's/ //g' | sed 's/$/\t\!/g' | cat >> noun.todo

noe=`grep -c '' noun.todo`
noe=`expr $noe - $noe_`
echo "$noe entries added to todo list"
