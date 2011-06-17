#!/bin/bash

#backup previous copy of "proper-noun.todo"
cat fresh.proper-noun | cat > fresh.proper-noun_back
echo "--------------"


#tag
n=`grep -c "" proper-noun.bn.patch`
if [ $n -gt 0 ]; then
	cat fresh.proper-noun | grep -v "\!" | ./create_proper-noun_monodix_entry.py > /tmp/bar6
fi

#append to patch fle
if [ -f proper-noun.bn.patch ]; then
	noe_=`grep -c "" proper-noun.bn.patch`
else
	noe_=`expr 0`
fi

noe=`grep -c "" /tmp/bar6`

if [ $noe -gt 0 ]; then
	echo "    <!-- proper-nouns added @ "`date --utc`" -->" >> proper-noun.bn.patch
	cat /tmp/bar6 | cat >> proper-noun.bn.patch
	noe_=`expr $noe_ + 1`
fi

noe=`grep -c "" proper-noun.bn.patch`
noe=`expr $noe - $noe_`
echo "patched  : $noe"

#remove from todo file
cat fresh.proper-noun | grep '\!' > /tmp/bar6
cat /tmp/bar6 > fresh.proper-noun

noe=`grep -c "" fresh.proper-noun`
echo "remaining: $noe"
echo "--------------"
