#!/bin/sh
egrep -v '\#|\?|\!' - | perl -pe 's/<(\w+)>/<s n="$1">/g' | awk -F'\t' '{ print "<e><p><l>"$1"</l><r>"$2"<s n=\"n\"/></r></p></e>" }'
