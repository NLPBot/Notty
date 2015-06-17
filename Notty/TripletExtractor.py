from nltk.tree import *
from sets import Set

class TripletExtractor(object):
	"""docstring for TripletExtractor"""
	def __init__(self, tree):
		self.tree = tree
		self.max_level = 0
		self.deepest_verb = None
	
	# Return a set consisting of triplet { subj, pred, obj }
	def extract(self):
		# First get all the sets
		subj = pred = obj = {}
		subj = self.extractSubject(self.getNPSubtree())
		pred = self.extractPredicate(self.getVPSubtree())
		obj = self.extractObject(self.getVPSiblings())
		# Handle Empty Sets
		if len(att)==0 or len(att)==0 or len(att)==0:
			return {}
		else:
			return att | subj | pred | obj

	# Returns a set containing attributes
	def extractAttribute(self,word):
		result = None
		# search among the word’s siblings 
		# if adjective(word) 
		if 'J' in word.label():
			# result <- all RB siblings 
			result = 
		# else
		else:
			# if noun(word) 
			if 'N' in word.label():
				# result <- all DT, PRP$, POS, JJ, CD, ADJP, QP, NP siblings
				result = 
			# else
			else:
				# if verb(word)
				if 'V' in word.label(): 
					# result <- all ADVP siblings
					result = 


		# search among the word’s uncles
		# if noun(word) or adjective(word) 
			# if uncle = PP 
				# result <- uncle subtree
		# else
			# if verb(word) and (uncle = verb) 
				# result <- uncle subtree
		# if result ≠ failure then return result else return failure

		return {}

	def extractSubject(self,subtree):
		# subject <- first noun found in NP_subtree
		subject = self.FindFirstNoun(subtree)
		# subjectAttributes <- EXTRACT-ATTRIBUTES(subject) 
		subjectAttributes = self.extractAttribute(subtree)
		# result <- subject | subjectAttributes
		result = subject | subjectAttributes
		# if result != failure then return result 
		# else return failure
		return result

	def extractPredicate(self,VP_subtree):
		# predicate <- deepest verb found in VP_subtree 
		predicate = Set(self.FindDeepestVerb(VP_subtree,0))
		# predicateAttributes <- EXTRACT-ATTRIBUTES(predicate) 
		predicateAttributes = self.extractAttribute(predicate)
		# result <- predicate | predicateAttributes 
		result = predicate | predicateAttributes
		# if result != failure then return result 
		# else return failure 
		return result

	def extractObject(self,VP_sbtree,siblings):
		# siblings <- find NP, PP and ADJP siblings of VP_subtree 
		# for each value in siblings do 
		object = None
		for value in siblings:
			value_label = value.label()
			# if value = NP or PP 
			if 'NP' in value_label or 'PP' in value_label:
				# object <- first noun in value
				object = self.FindFirstNoun()[0]
			# else
			if 'JJ' in value_label:
				# object <- first adjective in value
				object = value
			# objectAttributes <- EXTRACT-ATTRIBUTES(object) 
			objectAttributes = self.extractAttribute(object)
		# result <- object | objectAttributes 
		result = Set([object]) | objectAttributes
		# if result != failure then return result 
		# else return failure
		return result

	def getVPSubtree(self):
		for child in self.tree:
			if 'VP' in child.label():
				return child

	def getVPSiblings(self):
		siblings = []
		for child in self.tree:
			if 'VP' not in child.label():
				siblings.append(child)
		return siblings

	def getNPSubtree(self):
		for child in self.tree:
			if 'NP' in child.label():
				return child

	# Return first noun or none
	def FindFirstNoun(self,subtree):
		first_noun = {}
		NP_tree = None
		for child in subtree:
			if 'NP' in child.label(): 
				NP_tree = child
		for n in NP_tree:
			if 'NN' in n.label():
				first_noun.add(n)
		return first_noun

	# Return deepest verb or none
	def FindDeepestVerb(self,VP_subtree,level):
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
					print('      finally    '+str(verb[0]))
					if len(verb)>1 and verb[1]>=self.max_level:
						print('      updating max_level       ' + str(self.max_level) + str(verb[0]))
						self.deepest_verb = verb[0]
						self.max_level = verb[1]
			return self.deepest_verb
