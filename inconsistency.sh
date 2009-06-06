TMPDIR=/tmp
lt-expand apertium-bn-en.en.dix | grep -v '<prn><enc>' | grep -e ':<:' -e '\w:\w' | sed 's/:<:/%/g' | sed 's/:/%/g' | cut -f2 -d'%' |  sed 's/^/^/g' | sed 's/$/$ ^.<sent>$/g' | tee $TMPDIR/tmp_testvoc1.txt |
        apertium-pretransfer|
        apertium-transfer apertium-bn-en.en-bn.t1x  en-bn.t1x.bin  en-bn.autobil.bin |
        apertium-interchunk apertium-bn-en.en-bn.t2x  en-bn.t2x.bin |
        apertium-postchunk apertium-bn-en.en-bn.t3x  en-bn.t3x.bin  | tee $TMPDIR/tmp_testvoc2.txt |
        lt-proc -d en-bn.autogen.bin > $TMPDIR/tmp_testvoc3.txt
paste -d _ $TMPDIR/tmp_testvoc1.txt $TMPDIR/tmp_testvoc2.txt $TMPDIR/tmp_testvoc3.txt | sed 's/\^.<sent>\$//g' | sed 's/_/   --------->  /g'
