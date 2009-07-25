#!/bin/sh

# adjective speling
../speling-paradigms.py adjective.bn.speling > /tmp/adjective.bn.dix
../paradigm-chopper.py /tmp/adjective.bn.dix > adjective.bn.dix

# also generate the expand
lt-expand adjective.bn.dix > adjective.bn.expand
