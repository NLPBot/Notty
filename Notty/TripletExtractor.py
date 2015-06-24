from nltk.tree import *
from sets import Set

class TripletExtractor(object):
	"""docstring for TripletExtractor"""
	def __init__(self, tree):
		self.tree = tree
		self.max_level = 0
		self.deepest_verb = None
		self.first_noun = None
	
	# Return a set consisting of triplet [ subj, pred, obj ]
	def extract(self):
		#print(' WITHIN extract ...... ')
		# First get all the sets
		subj = pred = obj = []
		subj = self.extractSubject(self.getNPSubtree())
		pred = self.extractPredicate(self.getVPSubtree())
		obj = obj + self.extractObject()
		# Handle Empty Sets
		if subj==None or pred==None or obj==None:
			return []
		if len(subj)==0 or len(pred)==0 or len(obj)==0: 
			return []
		else:
			return (subj+pred+obj)

	# Returns a list containing attributes
	def extractAttribute(self,word):
		#print(' WITHIN extractAttribute ...... ')
		result = []
		if word==None:
			return result
		# Get siblings
		siblings = self.getSiblings(self.tree,word)
		uncles = self.getUncles(self.tree,word)

		# if adjective(word) 
		if 'J' in word.label():
			# result <- all RB siblings 
			result = result + self.getRBSiblings(siblings)[0]
		# else
		else:
			# if noun(word) 
			if 'N' in word.label():
				# result <- all DT, PRP$, POS, JJ, CD, ADJP, QP, NP siblings
				result = result + self.getMANYSiblings(siblings)
			# else
			else:
				# if verb(word)
				if 'V' in word.label(): 
					# result <- all ADVP siblings
					result = result + self.getADVPSiblings(siblings)
		for uncle in uncles:
			# if noun(word) or adjective(word) 
			if 'N' in word.label() or 'J' in word.label():
				# if uncle = PP 
				if 'PP' in uncle.label():
					# result <- uncle subtree
					result.append(uncle)
			# else
			else:
				# if verb(word) and (uncle = verb) 
				if 'V' in word.label() and 'V' in uncle.label():
					# result <- uncle subtree
					result.append(uncle)
		# if result != failure then return result else return failure
		return result

	def extractSubject(self,subtree):
		#print(' WITHIN extractSubject ...... '+str(subtree))
		# subject <- first noun found in NP_subtree
		if self.FindFirstNoun(self.tree)==None:
			return []
		else:
			result = subject = []
			# subject <- first noun found in NP_subtree 
			subject.append(self.first_noun)
			# subjectAttributes <- EXTRACT-ATTRIBUTES(subject) 
			subjectAttributes = self.extractAttribute(subtree)
			# result <- subject | subjectAttributes
			result = subject + subjectAttributes
			# if result != failure then return result else return failure
			return result

	def extractPredicate(self,VP_subtree):
		#print(' WITHIN extractPredicate ...... ')
		# predicate <- deepest verb found in VP_subtree 
		predicate = self.FindDeepestVerb(VP_subtree,0)
		# predicateAttributes <- EXTRACT-ATTRIBUTES(predicate) 
		predicateAttributes = self.extractAttribute(predicate)
		# result <- predicate | predicateAttributes 
		result = [predicate] + predicateAttributes
		# if result != failure then return result else return failure 
		return result

	def extractObject(self):
		#print(' WITHIN extractObject ...... ' + str(VP_sbtree))
		raw_siblings = self.getSiblings(self.tree,self.deepest_verb)
		siblings = []
		for VPSibling in raw_siblings:
			if 'NP' in VPSibling.label() or 'PP' in VPSibling.label() or 'ADJP' in VPSibling.label():
				siblings.append(VPSibling)
		# siblings <- find NP, PP and ADJP siblings of VP_subtree 
		# for each value in siblings do 
		result = []
		object = None
		for sib in siblings:
			value_label = sib.label()
			# if value = NP or PP 
			if 'NP' in value_label or 'PP' in value_label:
				# object <- first noun in value
				if self.FindFirstNoun(sib):
					object = self.first_noun
			# else
			if 'JJ' in value_label:
				# object <- first adjective in value
				object = sib
			# objectAttributes <- EXTRACT-ATTRIBUTES(object) 
			objectAttributes = self.extractAttribute(object)
		# result <- object | objectAttributes 
		if object==None:
			return result
		else:
			#return [object] + objectAttributes
			return [object]

	# Get Uncles
	def getUncles(self,tree,ref):
		#print(' WITHIN getUncles ...... ')
		uncles = []
		if (tree.height())==2:
			return uncles
		found = False
		for child in tree:
			if ref==child:
				found = True
				break
			else:
				uncles = uncles + self.getUncles(child,ref)
		if found == True:
			#print(' father is ' + str(tree))
			uncles = self.getSiblings(self.tree,tree)
		return uncles

	# Get siblings
	def getSiblings(self,tree,ref):
		#print(' WITHIN getSiblings ...... ')
		siblings = []
		if (tree.height())==2:
			return siblings
		found = False
		for child in tree:
			try:
				if ref==child:
					found = True
					break
			except AttributeError:
				print('AttributeError!')
				return siblings
			siblings = siblings + self.getSiblings(child,ref)
		if found == True:
			for child in tree:
				if not(ref==child):
					siblings.append(child)
		return siblings

	# Get VP subtree
	def getVPSubtree(self):
		#print(' WITHIN getVPSubtree ...... ')
		for child in self.tree:
			if 'VP' in child.label():
				return child

	# Find NP, PP and ADJP 
	def getVPSiblings(self):
		#print(' WITHIN getVPSiblings ...... ')
		siblings = []
		for child in self.tree:
			if 'NP' in child.label() or 'PP' in child.label() or 'ADJP' in child.label():
				siblings.append(child)
		return siblings

	def getNPSubtree(self):
		#print(' WITHIN getNPSubtree ...... ')
		for child in self.tree:
			if 'NP' in child.label():
				return child

	def getRBSiblings(self,siblings):
		#print(' WITHIN getRBSiblings ...... ')
		RBs = []
		for sibling in siblings:
			if 'RB' in sibling.label(): 
				RBs.append(sibling)
		return RBs

	# all DT, PRP$, POS, JJ, CD, ADJP, QP, NP siblings
	def getMANYSiblings(self,siblings):
		#print(' WITHIN getMANYSiblings ...... ')
		RBs = []
		for sibling in siblings:
			if 'DT' in sibling.label() or 'PRP' in sibling.label() or 'POS' in sibling.label() or 'JJ' in sibling.label(): 
				RBs.append(sibling)
			if 'ADJP' in sibling.label() or 'QP' in sibling.label() or 'NP' in sibling.label() or 'CD' in sibling.label():
				RBs.append(sibling)
		return RBs

	# getADVPSiblings
	def getADVPSiblings(self,siblings):
		#print(' WITHIN getADVPSiblings ...... ')
		RBs = []
		for sibling in siblings:
			if 'ADVP' in sibling.label(): 
				RBs.append(sibling)
		return RBs

	# Return first noun or none
	def FindFirstNoun(self,subtree):
		#print(' WITHIN FindFirstNoun ...... ')
		for child in subtree:
			if 'NP' in child.label():
				return self.FindFirstNoun(child)
			if 'NN' in child.label() or 'PRP' in child.label():
				self.first_noun = child
				break
		return self.first_noun

	# Return deepest verb or none
	def FindDeepestVerb(self,VP_subtree,level):
		#print(' WITHIN FindDeepestVerb ...... ')
		level += 1
		if len(VP_subtree)==1:
			if 'V' in VP_subtree.label():
				return [VP_subtree,level]
			else:
				return [level]
		else: 
			VP_tree = None
			for child in VP_subtree:
				if 'V' in child.label(): # Only look within verb branches 
					verb = self.FindDeepestVerb(child,level)
					#print('      finally    '+str(verb[0]))
					if len(verb)>1 and verb[1]>=self.max_level:
						#print('      updating max_level       ' + str(self.max_level) + str(verb[0]))
						self.deepest_verb = verb[0]
						self.max_level = verb[1]
			return self.deepest_verb
