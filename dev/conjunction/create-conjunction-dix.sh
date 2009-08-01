#!/bin/sh

cat conjuction.bn.list | awk -F\t '{ print $1"; "$1";; cnjcoo" }' > conjuction.bn.speling
sh to-dix-quick.sh conjuction.bn.speling > conjuction.bn.dix
