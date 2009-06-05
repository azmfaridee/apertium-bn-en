#!/bin/bash

cat bdict.db | grep -P ":CC|:CD|:DT|:EX|:FW|:IN|:JJ|:JJR|:JJS|:LS|:MD|:NN|:NNS|:NP|:NPS|:PDT|:POS|:PP|:PP$|:RB|:RBR|:RBS|:RP|:SYM|:TO|:UH|:VB|:VBD|:VBG|:VBN|:VBP|:VBZ|:WDT|:WP|:WP$|:WRB|:VV" > tagged

cat bdict.db | grep -P -v ":CC|:CD|:DT|:EX|:FW|:IN|:JJ|:JJR|:JJS|:LS|:MD|:NN|:NNS|:NP|:NPS|:PDT|:POS|:PP|:PP$|:RB|:RBR|:RBS|:RP|:SYM|:TO|:UH|:VB|:VBD|:VBG|:VBN|:VBP|:VBZ|:WDT|:WP|:WP$|:WRB|:VV" > untagged



