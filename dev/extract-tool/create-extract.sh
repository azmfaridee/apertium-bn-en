#!/bin/bash

python apertium2extract.py ../../apertium-bn-en.bn.dix | python reformat.py > apertium-bn-en.bn.dix.extract