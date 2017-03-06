#!/bin/python3.4

import sys
import re
import pdb

def getPronouns(t):
	pronouns = []

	for st in t.subtrees():
		if st.label().unicode_repr().split('[')[0] in ['PRP', 'PossPro'] and len(st.leaves()) == 1:
			pronouns.append(st)

	return pronouns

def getImmediateNominal(t):
	for st in t.subtrees():
		if st.label().unicode_repr().split('[')[0] in ['Nom', 'PRP']:
			return st

def sanitize(raw):
	return re.sub(' +', ' ', str(raw).replace('\n', ''))

def printInputs(d, p):
	sys.stdout.write(p.leaves()[0]+'\t')
	for c in d:
		sys.stdout.write(sanitize(c)+' ')
	sys.stdout.write('\n')

def nextX(c, path=[]):

	while True:
		path.append(c)
		c = c.parent()
		if c is None:
			sys.stdout.write('Unable to find next X.\n')
		if c.label().unicode_repr().split('[')[0] in ['NP', 'S']:
			break

	sys.stdout.write(sanitize(c)+'\n')				
	return c, path

def checkCandidate(a, p):
	sys.stdout.write(sanitize(a)+'\n')				
	sys.stdout.write('Reject - TBD\n')
	return False

def lrbfTraverse(t, p, path=[], targetLeftOfPath=True, separatedByNPorS=True):

	"""
	@desc	- Traversal manager -- conducts left-ot-right, breadth-first
		  traversals with respect to tree 't'. Includes various options 
	          to accomodate step-specific requirements.
	@param	- t: root node defining the tree to be traversed
	@param	- p: target pronoun, the features of which are needed to qualify the
		  antecedent
	@param	- targetLeftOfPath: 'True' if targeting portion of tree below 't' left of 
		  path *or* if no path is applicable. 'False' if targeting right-hand
		  portion of the tree.
	@param 	- path: unordered list of node references through which the has cursor
		  passed while on its way to X. (leave as empty if no path applies)
	@param	- separatedByNPorS: implements the proxy binding contraint from step 3.
		  Leave unspecified if the constraint is not applicable.
	@return	- found: 'True' if resolution was successful; else 'False'
	"""

	rightOfPath = False
	tapped = [t]
	queue = [(t, separatedByNPorS)]
	qualifiedNodes = []

	while len(queue) > 0:
		current = queue.pop(0)
		for node in current[0]:

			if node in path:
				if targetLeftOfPath:
					break						#The path has been hit while exploring the lhs - explore this parent no further
				else:
					rightOfPath = True       			#The path has been hit while exploring the rhs - turn on the listener
					continue					#Provided the tree is proper, the listener can remain on after the inital switch
				if not targetLeftOfPath and not rightOfPath: 		#The listener is off while exploring the rhs - try the next one 
					continue
			if type(node) is str:						#Reached a terminal; nothing to check
				continue

			if node.label().unicode_repr().split('[')[0] == 'NP':					#Potential candidate 
				if current[1]:						#Step-3 check (Effectively skipped by default)
					found = checkCandidate(node, p)
					if found:
						return True

			if node not in tapped:
				tapped.append(node)
				sepStat = current[1] or node.label().unicode_repr().split('[')[0] in ['NP', 'S']
				queue.append((node, sepStat))
	return False
