for paraula in `cat $1 | cut -f1 -d';' | sed 's/ /_/g'`; do 
	LEM=`echo $paraula | sed 's/_/ /g'`;
	LEMI=`echo $paraula | sed 's/_/<b\/>/g'`;

	echo '    <e lm="'$LEM'"><i>'$LEMI'</i><par n="ও__adv"/></e>';
done
