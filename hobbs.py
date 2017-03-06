#!/bin/python3.4

import resources as rc
import sys

		# Steps 

def step1(c):

	"""
	@desc	- Begin at the noun phrase (NP) node immediately dominating the pronoun	
	@param	- c: parented-tree preterminal node containing the target pronoun
	@return	- c: NP node immediately dominating p
	"""

	while True:
		c = c.parent()
		if c.label().unicode_repr().split('[')[0] == 'NP':
			break
	return c

def step2(c):

	"""
	@desc	- Go up the tree to the first NP or sentence (S) node encountered. 
		  Call this node X, and call the path to reach it p.
	@param	- c: parentedTree node over which the cursor is currently resting
	@return	- x: parentedTree node corresponding to 'X' in the description
	@return	- path: unordered list of node references through which the cursor
		  passes while on its way to X. 
	"""

	return rc.nextX(c)

def step3(x, p, path):

	"""
	@desc	- Traverse all branches below node X to the left of path p 
		  in a left-to-right, breadth-first fashion. Propose as the 
		  antecedent any encountered NP node that has an NP or S node 
		  between it and X.
		  Achieve this effect vis-a-vis lrbfTraverse by setting the
		  separatedByNPorS to 'False' upon the first call.
	@param	- x: parentedTree node corresponding to 'X' in the description
	@param 	- path: unordered list of node references through which the cursor
		  passes while on its way to X. 
	@return	- found: 'True' if resolution was successful; else 'False'
	"""

	return rc.lrbfTraverse(x, p, path, True, False)

def step4(d, p):

	i = len(d) - 2
	while i >= 0:
		sys.stdout.write(rc.sanitize(d[i])+'\n')				
		rc.lrbfTraverse(d[i], p)
		i -= 1

def step5(x):
	return rc.nextX(x)

def step6(x, p, path):
	if rc.getImmediateNominal(x) not in path:
		return rc.checkCandidate(x, p)

def step7(x, p, path):
	return rc.lrbfTraverse(x, p, path, True, True)

def step8(x, p, path):
	return rc.lrbfTraverse(x, p, path, False, True)

		# Main 

def resolvePronoun(d, p):

	c = step1(p)
	x, path = step2(c)
	if step3(x, p, path) is True:
		return

	while True:

		if x.parent() is None:
			break

		x, path = step5(x, path)

		if step6(x, p, path) is True:
			return

		if step7(x, p, path) is True:
			return

		if step8(x, p, path) is True:
			return

	step4(d, p)
