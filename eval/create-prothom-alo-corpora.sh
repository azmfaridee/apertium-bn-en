#!/bin/sh

DETAILS=/home/zaher/Desktop/GSoC09/crawler/prothom-alo/prothom-alo.com/detail/news/
#CORPORA=/home/zaher/Desktop/GSoC09/apertium/prothom-alo-eval/prothom-alo-corpora.txt
CORPORA=/home/zaher/Desktop/GSoC09/apertium/coverage-check/prothom-alo-corpora.txt

rm -f $CORPORA;
touch $CORPORA;

for x in `ls $DETAILS`; do 
	cat $DETAILS/$x | perl -pe 's/(\s)+/\1/g' | perl -pe 's/\n|\t//g' | \
	perl -ne "print m/<div class=\"alternative.*?\">.*?<\/div>/g" | \
	perl -pe 's/<div class=\"alternative.*?\">|<\/div>//g' | \
	perl -ne 's/<br \/>/\n/g; print "$_\n\n"'; 
done >> $CORPORA


