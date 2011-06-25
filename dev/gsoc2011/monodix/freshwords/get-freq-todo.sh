#!/bin/bash

cut -f2 | lt-proc -a ../../../../bn-en.automorf.bin | grep "*" | sed 's/.*\*//g' | sed 's/\$//g' | grep -v "[a-z]" | sed 's/$/\t\!/g'
