#!/bin/bash

# with the new lemmas listed along with there mapping pardefs in 'fresh.noun', this script
# generates the correspoding monodix entries running 'create_noun_monodix_entry.py' and then
# patches it to the end of the 'noun.patch' with a comment header
# note: 'fresh.noun' has the following format:
# lemma<comma>pardefid			where pardefid is defined in 'noun.pardef'
# and an entry with '!' in place of 'pardefid' is ignored



#backup previous copy of "noun.todo"
cat fresh.noun | cat > fresh.noun_back
echo "--------------"

#tag
n=`grep -c "" noun.bn.patch`
if [ $n -gt 0 ]; then
	cat fresh.noun | grep -v "\!" | ./create_noun_monodix_entry.py > /tmp/bar6
fi

#append to patch fle
if [ -f noun.bn.patch ]; then
	noe_=`grep -c "" noun.bn.patch`
else
	noe_=`expr 0`
fi

noe=`grep -c "" /tmp/bar6`

if [ $noe -gt 0 ]; then
	echo "    <!-- nouns added @ "`date --utc`" -->" >> noun.bn.patch
	cat /tmp/bar6 | cat >> noun.bn.patch
	noe_=`expr $noe_ + 1`
fi

noe=`grep -c "" noun.bn.patch`
noe=`expr $noe - $noe_`
echo "patched  : $noe"

#remove from todo file
cat fresh.noun | grep '\!' > /tmp/bar6
cat /tmp/bar6 > fresh.noun

noe=`grep -c "" fresh.noun`
echo "remaining: $noe"
echo "--------------"
