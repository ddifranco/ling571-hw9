#!/bin/bash

#GRAMMAR='/opt/dropbox/16-17/571/hw9/grammar.cfg'
#GRAMMAR='modified_grammar.fcfg'
GRAMMAR='grammar.fcfg'
TESTS='/opt/dropbox/16-17/571/hw9/coref_sentences.txt'
OUTPUT='prelim.txt'

./main.py  $GRAMMAR $TESTS $OUTPUT
