#!/bin/bash

# provide the corpus file as the only argument, with the format like this: "english_sentence.*reference_sentence" per line
# usage: sh quantitative_analysis.sh test-data1.txt

HOME="../"

N=`cat $1 | sed 's/[\.].*//g' | wc -w`
printf "%-3s = %d\n" "N" $N

cat $1 | sed 's/.*[\.]\*//g' | sed 's/[\.]//g' > /tmp/abc1
cat $1 | sed 's/\*.*//g' | apertium -d $HOME en-bn | sed 's/[\.]//g' > /tmp/abc2
paste /tmp/abc1 /tmp/abc2 -d* > /tmp/abc3

SDI=$(python levenshtein.py /tmp/abc3)
WER=$(echo "scale=4;($SDI / $N)*100" | bc)
printf "%-3s = %.2lf%%\n" "WER" $WER

O=`cat /tmp/abc2 | grep -c "[\*|\#|\@]"`
OOV=$(echo "scale=4;($O/$N)*100" | bc)
printf "%-3s = %.2lf%%\n" "OOV" $OOV




