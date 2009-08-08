#!/bin/sh

# adjective speling
cat adjective.bn.speling adjective-extra.bn.speling > /tmp/adjective.bn.speling
../speling-paradigms.py /tmp/adjective.bn.speling > /tmp/adjective.bn.dix
../paradigm-chopper.py /tmp/adjective.bn.dix > adjective.bn.dix

# also generate the expand
lt-expand adjective.bn.dix > adjective.bn.expand
