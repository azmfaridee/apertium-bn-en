#!/bin/sh

# postposition speling
../speling-paradigms.py postposition.bn.speling > /tmp/postposition.bn.dix
../paradigm-chopper.py /tmp/postposition.bn.dix > postposition.bn.dix
