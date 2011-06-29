#!/bin/bash


grep -v "[\!\?]" | python ../../../tools/fix-spelling.py | ./distribute_words.py
echo "--------------------"


#adjectives
adj=`grep -c '' ../adjective/fresh.adj`
cat ../adjective/adjective.bn.dix | grep "<e.*lm" | sed 's/.*<i>//g' | sed  's/<\/i>.*//g' > /tmp/adjs
cat ../adjective/fresh.adj | sed 's/,/\t/g' | cut -f1 | cat >> /tmp/adjs
cat /tmp/fresh.adj | python ../../../uniq.py | grep -v -w -f /tmp/adjs | sed 's/$/,\!/g' | cat  >> ../adjective/fresh.adj
adj1=`grep -c '' ../adjective/fresh.adj`
adj=`expr $adj1 -  $adj`
echo "adjectives: $adj"


#nouns
n=`grep -c '' ../noun/fresh.noun`
cat ../noun/noun.bn.dix | grep "<e.*lm" | sed 's/.*<i>//g' | sed  's/<\/i>.*//g' > /tmp/nouns
cat ../noun/fresh.noun | sed 's/,/\t/g' | cut -f1 | cat >> /tmp/nouns
cat /tmp/fresh.noun | python ../../../uniq.py | grep -v -w -f /tmp/nouns | sed 's/$/,\!/g' | cat  >> ../noun/fresh.noun
n1=`grep -c '' ../noun/fresh.noun`
n=`expr $n1 -  $n`
echo "nouns: $n"


#proper-nouns
np=`grep -c '' ../proper-noun/fresh.proper-noun`
cat ../proper-noun/proper-noun.bn.dix | grep "<e.*lm" | sed 's/.*<i>//g' | sed  's/<\/i>.*//g' > /tmp/proper-nouns
cat ../proper-noun/fresh.proper-noun | sed 's/,/\t/g' | cut -f1 | cat >> /tmp/proper-nouns
cat /tmp/fresh.proper-noun | python ../../../uniq.py | grep -v -w -f /tmp/proper-nouns | sed 's/$/,\!/g' | cat  >> ../proper-noun/fresh.proper-noun
np1=`grep -c '' ../proper-noun/fresh.proper-noun`
np=`expr $np1 -  $np`
echo "proper-nouns: $np"


#adverbs
adv=`grep -c '' ../adverb/fresh.adv`
cat ../adverb/adverb.bn.dix | grep "<e.*lm" | sed 's/.*<i>//g' | sed  's/<\/i>.*//g' > /tmp/adjv
cat ../adverb/fresh.adv | sed 's/,/\t/g' | cut -f1 | cat >> /tmp/adjv
cat /tmp/fresh.adv | python ../../../uniq.py | grep -v -w -f /tmp/adjv | sed 's/$/,\!/g' | cat  >> ../adverb/fresh.adv
adv1=`grep -c '' ../adverb/fresh.adv`
adv=`expr $adv1 -  $adv`
echo "adverbs: $adv"


echo "--------------------"
tot=`expr $adj + $n + $np + $adv`
echo "total: $tot"
