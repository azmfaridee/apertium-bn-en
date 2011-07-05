#!/bin/bash

# with the new lemmas listed along with there mapping pardefs in 'fresh.adv', this script
# generates the correspoding monodix entries running 'create_adv_monodix_entry.py' and then
# patches it to the end of the 'noun.patch' with a comment header
# note: 'fresh.adv' has the following format:
# lemma<comma>pardefid			where pardefid is defined in 'adv.pardef'
# and an entry with '!' in place of 'pardefid' is ignored

#backup previous copy of "adv.todo"
cat fresh.adv | cat > fresh.adv_back
echo "--------------"


#tag
n=`grep -c "" adv.bn.patch`
if [ $n -gt 0 ]; then
	cat fresh.adv | grep -v "\!" | ./create_adv_monodix_entry.py > /tmp/bar6
fi

#append to patch fle
if [ -f adv.bn.patch ]; then
	noe_=`grep -c "" adv.bn.patch`
else
	noe_=`expr 0`
fi

noe=`grep -c "" /tmp/bar6`

if [ $noe -gt 0 ]; then
	echo "    <!-- Adverbs added @ "`date --utc`" -->" >> adv.bn.patch
	cat /tmp/bar6 | cat >> adv.bn.patch
	noe_=`expr $noe_ + 1`
fi

noe=`grep -c "" adv.bn.patch`
noe=`expr $noe - $noe_`
echo "patched  : $noe"

#remove from todo file
cat fresh.adv | grep '\!' > /tmp/bar6
cat /tmp/bar6 > fresh.adv

noe=`grep -c "" fresh.adv`
echo "remaining: $noe"
echo "--------------"
