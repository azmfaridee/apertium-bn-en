#!/bin/bash

cat ./resultset.csv | awk -F',' '{print $1"; "$3"; "$4"; "$2 }' > determiner.bn.speling
