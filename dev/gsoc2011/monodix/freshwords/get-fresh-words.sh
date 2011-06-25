#!/bin/bash

grep -v "\!" | ./distribute_words.py

cat ../adjective/adjective.bn.dix | grep "<e.*lm" | sed 's/.*<i>//g' | sed  's/<\/i>.*//g' > /tmp/adjs
cat ../adjective/fresh.adj | sed 's/,/\t/g' | cut -f1 | cat >> /tmp/adjs
cat /tmp/fresh.adj | python ../../../uniq.py | grep -v -w -f /tmp/adjs | sed 's/$/,\!/g' | cat  >> ../adjective/fresh.adj

cat ../noun/noun.bn.dix | grep "<e.*lm" | sed 's/.*<i>//g' | sed  's/<\/i>.*//g' > /tmp/nouns
cat ../noun/fresh.noun | sed 's/,/\t/g' | cut -f1 | cat >> /tmp/nouns
cat /tmp/fresh.noun | python ../../../uniq.py | grep -v -w -f /tmp/nouns | sed 's/$/,\!/g' | cat  >> ../noun/fresh.noun

cat ../proper-noun/proper-noun.bn.dix | grep "<e.*lm" | sed 's/.*<i>//g' | sed  's/<\/i>.*//g' > /tmp/proper-nouns
cat ../proper-noun/fresh.proper-noun | sed 's/,/\t/g' | cut -f1 | cat >> /tmp/proper-nouns
cat /tmp/fresh.proper-noun | python ../../../uniq.py | grep -v -w -f /tmp/proper-nouns | sed 's/$/,\!/g' | cat  >> ../proper-noun/fresh.proper-noun
