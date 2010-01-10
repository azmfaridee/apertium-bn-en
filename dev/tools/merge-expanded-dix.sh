#!/bin/sh

# This script takes a folder as an argument that contains several expand files,
# then creates dix out of them by using expand-paradigms.py and then merges them
# using xpath

# FIXME:
# In Ubuntu xpath supports optional switch that can prepend some extra text
# in front of the output, but Mac OS X xpath does not support any switch, So the
# following statement works in Linux but does not work in Mac OS X
# # xpath -p '    ' -e '/dictionary/pardefs/pardef[@n!="enclitic"]' $x
# So we use alternate expression to do the job for now
# # xpath $x '/dictionary/pardefs/pardef[@n!="enclitic"]' | | awk '{print "    "$0 }'

if [ $# -ne 1 ]; then
	echo 'Usage: sh merge-expanded-dix.sh <folder-containing-expand-files>'
	exit 1
fi

echo '<dictionary>
  <pardefs>'
for x in $(ls $1/*.expand); do
	cat $x | python expand-paradigms.py | \
	xpath '/dictionary/pardefs/pardef[@n!="enclitic"]' 2> /dev/null | \
	awk '{print "    "$0 }'
done
echo '  </pardefs>
  <section id="main" type="standard">'
for x in $(ls $1/*.expand); do
	cat $x | python expand-paradigms.py | \
	xpath '/dictionary/section/e' 2> /dev/null | awk '{print "    "$0 }'
done
echo '  </section>
</dictionary>'