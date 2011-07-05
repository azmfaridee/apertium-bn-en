#!/bin/bash

# with the new lemmas listed along with there mapping pardefs in 'fresh.adj', this script
# generates the correspoding monodix entries running 'create_adj_monodix_entry.py' and then
# patches it to the end of the 'adj.patch' with a comment header
# note: 'fresh.adj' has the following format:
# lemma<comma>pardefid			where pardefid is defined in 'adj.pardef'
# and an entry with '!' in place of 'pardefid' is ignored

#backup previous copy of "adj.todo"
cat fresh.adj | cat > fresh.adj_back
echo "--------------"


#tag
n=`grep -c "" adj.bn.patch`
if [ $n -gt 0 ]; then
	cat fresh.adj | grep -v "\!" | ./create_adj_monodix_entry.py > /tmp/bar6
fi

#append to patch fle
if [ -f adj.bn.patch ]; then
	noe_=`grep -c "" adj.bn.patch`
else
	noe_=`expr 0`
fi

noe=`grep -c "" /tmp/bar6`

if [ $noe -gt 0 ]; then
	echo "    <!-- Adjectives added @ "`date --utc`" -->" >> adj.bn.patch
	cat /tmp/bar6 | cat >> adj.bn.patch
	noe_=`expr $noe_ + 1`
fi

noe=`grep -c "" adj.bn.patch`
noe=`expr $noe - $noe_`
echo "patched  : $noe"

#remove from todo file
cat fresh.adj | grep '\!' > /tmp/bar6
cat /tmp/bar6 > fresh.adj

noe=`grep -c "" fresh.adj`
echo "remaining: $noe"
echo "--------------"
