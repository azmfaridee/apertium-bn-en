echo '<dictionary>
  <pardefs>
    <pardef n="এর__post">
      <e>
        <p>
          <l />
          <r><s n="post" /></r>
        </p>
      </e>
    </pardef>
  </pardefs>
  <section id="main" type="standard">';

for paraula in `cat $1 | cut -f1 -d';' | sed 's/ /_/g'`; do 
	LEM=`echo $paraula | sed 's/_/ /g'`;
	LEMI=`echo $paraula | sed 's/_/<b\/>/g'`;

	echo '    <e lm="'$LEM'"><i>'$LEMI'</i><par n="এর__post"/></e>';
done
echo '  </section>
</dictionary>';
