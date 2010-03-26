#!/bin/sh

# pronoun speling
#./create-speling-pronoun.py > pronoun.bn.speling
# there is some problem with pronoun, we cannot use the chopper now :(

../speling-paradigms.py pronoun.bn.speling_capfixed > /tmp/pronoun.bn.dix
../paradigm-chopper.py /tmp/pronoun.bn.dix > pronoun.bn.dix

#../speling-paradigms.py pronoun.bn.speling > pronoun.bn.dix

lt-expand pronoun.bn.dix > pronoun.bn.expand


