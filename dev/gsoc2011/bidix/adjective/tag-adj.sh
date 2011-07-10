#!/bin/bash

# 	generates the new bidix entries and appends to adj.patch by following
#		> filter adj.todo to move out the ambiguous entries to a seperate file ("adj.ambiguous")
#		> add tags to the filtered entries
#		> append the new tagged bidix entries to "adj.patch" with a comment header

#backup previous copy of "adj.todo"
cat adj.todo | cat > adj.todo_back
echo "--------------"
#filter out the ambiguous entries with '?' symbol
if [ -f adj.patch ]; then
	noe_=`grep -c "" adj.ambiguous`
else
	noe_=`expr 0`
fi
cat adj.todo | grep '?' | cat >> adj.ambiguous
noe=`grep -c "" adj.ambiguous`
noe=`expr $noe - $noe_`
echo "ambiguous: $noe"

#get lexical forms
cat adj.todo | egrep -v '\#|\?|\!' | cut -f2 | tee /tmp/bar1 |  lt-proc ../../../../en-bn.automorf.bin |  \
perl -pe 's/(\^)(.*?)(\/)//' | perl -pe 's/<comp>|<sup>//' | perl -pe 's/\/?\w*?(<vblex>|<n>|<adv>|<pr>|<prn>|<np>|<predet>)(<\w+>)*(\/|\$)?//g' | \
perl -pe 's/\$//g' > /tmp/bar2 && paste /tmp/bar1 /tmp/bar2 | awk '{ if($2 ~ /<adj>/) { print $0 } else { print $1"\t"$1"<adj>" } }' > /tmp/bar3

#tag
cat adj.todo | egrep -v '\#|\?|\!' | cut -f1 > /tmp/bar4 && cat /tmp/bar3 | cut -f2 | perl -pe 's/ /<b\/>/g' > /tmp/bar5
paste /tmp/bar4 /tmp/bar5 | perl -pe 's/<(\w+)>/<s n="$1"\/>/g' | awk -F'\t' '{ print "    <e><p><l>"$1"</l><r>"$2"</r></p></e>" }' > /tmp/bar6

#append to patch fle
if [ -f adj.patch ]; then
	noe_=`grep -c "" adj.patch`
else
	noe_=`expr 0`
fi

noe=`grep -c "" /tmp/bar6`

if [ $noe -gt 0 ]; then
	echo "    <!-- Adjectives added @ "`date --utc`" -->" >> adj.patch
	cat /tmp/bar6 | cat >> adj.patch
	noe_=`expr $noe_ + 1`
fi

noe=`grep -c "" adj.patch`
noe=`expr $noe - $noe_`
echo "patched  : $noe"

#remove from todo file
cat adj.todo | grep '!' > /tmp/bar6
cat /tmp/bar6 > adj.todo

noe=`grep -c "" adj.todo`
echo "remaining: $noe"
echo "--------------"
