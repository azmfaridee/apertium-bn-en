#!/bin/bash

#	populates the new bidix entries and appends to noun.patch by following
#		> filter noun.todo to move out the ambiguous entries
#		> add tags to the filtered entries
#		> append the new tagged bidix entries to noun.patch with a comment header

#backup previous copy of "noun.todo"
cat noun.todo | cat > noun.todo_back

echo "--------------"
#filter out the ambiguous entries with '?' symbol
if [ -f noun.patch ]; then
	noe_=`grep -c "" noun.ambiguous`
else
	noe_=`expr 0`
fi
cat noun.todo | grep '?' | cat >> noun.ambiguous
noe=`grep -c "" noun.ambiguous`
noe=`expr $noe - $noe_`
echo "ambiguous: $noe"

#get en lexical forms
cat noun.todo | egrep -v '\#|\?|\!' | cut -f2 | tee /tmp/bar1 |  lt-proc ../../../../en-bn.automorf.bin |  \
perl -pe 's/(\^)(.*?)(\/)//' | perl -pe 's/<sg>|<pl>//' | perl -pe 's/\/?\w*?(<vblex>|<adj>|<adv>|<pr>|<prn>|<np>|<predet>)(<\w+>)*(\/|\$)?//g' | \
perl -pe 's/\$//g' | perl -pe 's/\/.*//g' > /tmp/bar2 && paste /tmp/bar1 /tmp/bar2 | awk '{ if($2 ~ /<n>/) { print $0 } else { print $1"\t"$1"<n>" } }' > /tmp/bar3

#tag
cat noun.todo | egrep -v '\#|\?|\!' | cut -f1 > /tmp/bar4 && cat /tmp/bar3 | cut -f2 | 
perl -pe 's/ /<b\/>/g' > /tmp/bar5
paste /tmp/bar4 /tmp/bar5 | perl -pe 's/<(\w+)>/<s n="$1"\/>/g' | awk -F'\t' '{ print "    <e><p><l>"$1"</l><r>"$2"</r></p></e>" }' > /tmp/bar6

#append to patch fle
if [ -f noun.patch ]; then
	noe_=`grep -c "" noun.patch`
else
	noe_=`expr 0`
fi

noe=`grep -c "" /tmp/bar6`

if [ $noe -gt 0 ]; then
	echo "    <!-- Nouns added @ "`date --utc`" -->" >> noun.patch
	cat /tmp/bar6 | cat >> noun.patch
	noe_=`expr $noe_ + 1`
fi

noe=`grep -c "" noun.patch`
noe=`expr $noe - $noe_`
echo "patched  : $noe"

#remove from todo file
cat noun.todo | grep '!' > /tmp/bar6
cat /tmp/bar6 > noun.todo

noe=`grep -c "" noun.todo`
echo "remaining: $noe"
echo "--------------"
