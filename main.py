#!/bin/python3.4

import nltk
import sys
import re
import pdb
import resources as rc
import hobbs

grammar = nltk.data.load(sys.argv[1])
tests   = nltk.data.load(sys.argv[2])

ecp = nltk.parse.FeatureEarleyChartParser(grammar)
#f = open(sys.argv[3], 'w')

		# Main

blank = re.compile('^[ ]?[\r]?[\n]?$')
d = []
pronouns = []

for s in tests.split('\n'):

	if re.match(blank, s):
		print(pronouns)
		for p in pronouns:
			rc.printInputs(d, p)
			hobbs.resolvePronoun(d, p)
			sys.stdout.write('\n\n')
		d = []
		pronouns = []
		continue

	tkns = nltk.word_tokenize(s)
	
	result = nltk.tree.ParentedTree.convert(list(ecp.parse(tkns))[0])
	d.append(result)

	if len(d) >= 2:
		pronouns.extend(rc.getPronouns(result))
