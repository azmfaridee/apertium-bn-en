#!/bin/bash

HOME="."

echo "-----------------"
monodix=$(cat $HOME/apertium-bn-en.bn.dix | grep -c '<e lm')
printf "%-11s: %d\n" "MONODIX" $monodix

TD="dev/gsoc2011/monodix"
noun=$(cat $HOME/$TD/noun/noun.bn.patch | grep -c '<e lm')
printf "%-11s: %d\n" "noun" $noun
propernoun=$(cat $HOME/$TD/proper-noun/proper-noun.bn.patch | grep -c '<e lm')
printf "%-11s: %d\n" "proper-noun" $propernoun
adj=$(cat $HOME/$TD/adjective/adj.bn.patch | grep -c '<e lm')
printf "%-11s: %d\n" "adjective" $adj
adv=$(cat $HOME/$TD/adverb/adv.bn.patch | grep -c '<e lm')
printf "%-11s: %d\n" "adverb" $adv
t=$(echo "$monodix - $noun - $propernoun - $adj - $adv" | bc)
printf "%-11s: %d\n" "other" $t



echo ""
echo "-----------------"
bidix=$(cat $HOME/apertium-bn-en.bn-en.dix | grep -c '<e>')
printf "%-11s: %d\n" "BIDIX" $bidix


TD="dev/gsoc2011/bidix"
noun=$(cat $HOME/$TD/noun/noun.patch | grep -c '<e>')
printf "%-11s: %d\n" "noun" $noun
propernoun=$(cat $HOME/$TD/proper-noun/proper-noun.patch | grep -c '<e>')
printf "%-11s: %d\n" "proper-noun" $propernoun
adj=$(cat $HOME/$TD/adjective/adj.patch | grep -c '<e>')
printf "%-11s: %d\n" "adjective" $adj
t=$(echo "$monodix - $noun - $propernoun - $adj - $adv" | bc)
printf "%-11s: %d\n" "other" $t


echo ""
echo "-----------------"
