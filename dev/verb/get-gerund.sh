#!/bin/sh

# use this one line script to extract gerund from the verbs, then we can insert that into nouns list
cat verb.bn.expand | grep -e '<ger>' | grep -v -e '<adv>' | awk -F':' '{ print $1 }'
