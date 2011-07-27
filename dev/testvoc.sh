echo "==Bengali->English===========================";
sh inconsistency.sh bn-en > /tmp/bn-en.testvoc; sh inconsistency-summary.sh /tmp/bn-en.testvoc bn-en
echo ""
echo "==English->Bengali===========================";
sh inconsistency.sh en-bn > /tmp/en-bn.testvoc; sh inconsistency-summary.sh /tmp/en-bn.testvoc en-bn
