#!/bin/sh

# used to regenerate the element dix
regen_element_dix()
{
    echo "Regenerating the source dix" > /dev/stderr
    cd adjective; sh create-adjective-dix.sh
    cd ../adverb; sh create-adverb-dix.sh
    cd ../noun; sh create-noun-dix.sh
    cd ../postposition; sh create-postposition-dix.sh
    cd ../pronoun; sh create-pronoun-dix.sh
    cd ../proper-noun; sh create-proper-noun-dix.sh
    cd ../verb; sh create-verb-dix.sh
    cd ../determiner; sh create-determiner-dix.sh
    cd ../numerals; sh create-numerals-dix.sh
    cd ../conjuction; sh create-conjunction-dix.sh
    cd ..
}

os_depenedent_xpath_call()
{
	os=$(uname -s)
	echo -e "\n    $3\n"
	if [ $os = "Linux" ]; then
		xpath -p '    ' -e $1 $2
	elif [ $os = "Darwin" ]; then
		echo -n '    '
		# xpath somehow concatenates subsequent results and omits the newline
		# so have to manually add that, so we use two perl one liners to fix that
		xpath $2 $1 | perl -pe 's/<\/pardef><pardef/<\/pardef>\n    <pardef/g' | \
		perl -pe 's/<\/e><e/<\/e>\n    <e/g'
		echo -e "\n"
	fi
}

query_and_write()
{
	os_depenedent_xpath_call $1 adjective/adjective.bn.dix '<!-- Adjectives -->'
	os_depenedent_xpath_call $1 adverb/adverb.bn.dix '<!-- Adverbs -->'
    os_depenedent_xpath_call $1 noun/noun.bn.dix '<!-- Nouns -->'
    os_depenedent_xpath_call $1 postposition/postposition.bn.dix '<!-- Postpositions -->'
    os_depenedent_xpath_call $1 pronoun/pronoun.bn.dix '<!-- Pronouns -->'
    os_depenedent_xpath_call $1 proper-noun/proper-noun.bn.dix '<!-- Proper Nouns -->'
    os_depenedent_xpath_call $1 verb/verb.bn.dix '<!-- Verbs -->'
    os_depenedent_xpath_call $1 determiner/determiner.bn.dix '<!-- Determiners -->'
    os_depenedent_xpath_call $1 numerals/numerals.bn.dix '<!-- Numerals -->'
    os_depenedent_xpath_call $1 conjunction/conjuction.bn.dix '<!-- Conjunctions -->'
}

# uncomment if you changed something in the dix
#regen_element_dix

echo '<dictionary>  <alphabet>ঁংঃঅআইঈউঊঋঌএঐওঔকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহ়ঽািীুূৃৄেৈোৌ্ৎৗড়ঢ়য়ৠৡৢৣ০১২৩৪৫৬৭৮৯ৰৱ৲৳৴৵৶৷৸৹৺</alphabet>
  <sdefs>
    <sdef n="n"            c="Noun"/>
    <sdef n="np"           c="Proper noun"/>
    <sdef n="adj"          c="Adjective"/>
    <sdef n="num"          c="Numeral"/>
    <sdef n="prn"          c="Pronoun"/>
    <sdef n="det"          c="Determiner"/>
    <sdef n="adv"          c="Adverb"/>
    <sdef n="post"         c="Postposition"/>
    <sdef n="cnjcoo"       c="Co-ordinating conjunction"/>
    <sdef n="vblex"        c="Verb"/>

     <sdef n="al"           c="Altres"/>
     <sdef n="top"          c="Toponyms"/>
     <sdef n="ant"          c="Antroponyms"/>
     <sdef n="cog"          c="Cognomen"/>
     <sdef n="org"          c="Organisation"/>

    <sdef n="sint"         c="Synthetic"/>
    <sdef n="psint"        c="Partially synthetic"/>
    <sdef n="comp"         c="Comparative"/>
    <sdef n="sup"          c="Superlative"/>

    <sdef n="def"          c="Definite"/>
    <sdef n="dem"          c="Demonstrative"/>
    <sdef n="ref"          c="Reflexive"/>
    <sdef n="rel"          c="Relative"/>
    <sdef n="rec"          c="Reciprocal"/>
    <sdef n="qnt"          c="Quentifier"/>
    <sdef n="ind"          c="Indicative"/>

    <!-- will change this asap to itg -->
    <sdef n="int"          c="Interrogative"/>
    <sdef n="itg"          c="Interrogative"/>

    <sdef n="fam"          c="Familiar"/>
    <sdef n="infml"        c="Informal"/>
    <sdef n="pol"          c="Polite"/>

    <sdef n="m"            c="Masculine"/>
    <sdef n="f"            c="Feminine"/>
    <sdef n="mf"           c="Masculine / feminine"/>
    <sdef n="nt"           c="Neuter"/>

    <sdef n="nn"           c="Inanimate"/>
    <sdef n="aa"           c="Animate"/>
    <sdef n="an"           c="Animate / inanimate"/>
    <sdef n="hu"           c="Human"/>
    <sdef n="el"           c="Elite"/>

    <sdef n="sg"           c="Singular"/>
    <sdef n="pl"           c="Plural"/>
    <sdef n="sp"           c="Singular / plural"/>

    <sdef n="nom"          c="Nominative"/>
    <sdef n="obj"          c="Objective"/>
    <sdef n="gen"          c="Genitive"/>
    <sdef n="loc"          c="Locative"/>

    <sdef n="p1"           c="First person"/>
    <sdef n="p2"           c="Second person"/>
    <sdef n="p3"           c="Third person"/>
    <sdef n="impers"       c="Impersonal"/>

    <sdef n="inf"          c="Infinitive"/>
    <sdef n="ger"          c="Gerund"/>
    <sdef n="ft"           c="Future"/>
    <sdef n="pres"         c="Future"/>
    <sdef n="past"         c="Past"/>
    <sdef n="smpl"         c="Simple"/>
    <sdef n="pres"         c="Future"/>
    <sdef n="cnt"          c="Continuous"/>
    <sdef n="hbtl"         c="Habitual"/>
    <sdef n="prft"         c="Perfect"/>
    <sdef n="plprft"       c="Perfect"/>
    <sdef n="ppst"         c="Past Participle"/>
    <sdef n="pcnd"         c="Conditional Participle"/>
    <sdef n="imp"          c="Imperative"/>


    <sdef n="sent"         c="End of sentence marker"/>
  </sdefs>
  <pardefs>

    <!-- Punctuation -->

    <pardef n="separa">
      <e>
        <re>[.\?;:!।]</re>
        <p>
          <l/>
          <r><s n="sent"/></r>
        </p>
      </e>
    </pardef>

    <pardef n="numerals">
      <e>
        <re>[০১২৩৪৫৬৭৮৯]+</re>
        <p>
          <l/>
          <r><s n="num"/></r>
        </p>
      </e>
      <e>
        <re>[০১২৩৪৫৬৭৮৯]+</re>
        <p>
          <l>টা</l>
          <r><s n="num"/></r>
        </p>
      </e>
      <e>
        <re>[০১২৩৪৫৬৭৮৯]+</re>
        <p>
          <l>টি</l>
          <r><s n="num"/></r>
        </p>
      </e>
      <e>
        <re>[0-9]+([.,][0-9]+)?</re>
        <p>
          <l/>
         <r><s n="num"/></r>
        </p>
      </e>
    </pardef>


    <!-- Enclitics -->

    <pardef n="enclitic">
      <!-- passthrough -->
      <e>
        <p>
          <l />
          <r />
        </p>
      </e>
      <!-- Enclitic ই -->
      <e>
        <p>
          <l>ই</l>
          <r><j />ই<s n="adv" /></r>
        </p>
      </e>
      <!-- Enclitic ও -->
      <e>
        <p>
          <l>ও</l>
          <r><j />ও<s n="adv" /></r>
        </p>
      </e>
    </pardef>
'

# we want to remove the duplicate enclitics
query_and_write '/dictionary/pardefs/pardef[@n!="enclitic"]'

echo '  </pardefs>'
echo '  <section id="main" type="standard">'

query_and_write '/dictionary/section/e'

echo '  </section>'
echo '  <section id="final" type="inconditional">
    <e><par n="separa"/></e>
    <e><par n="numerals"/></e>
  </section>
</dictionary>'

