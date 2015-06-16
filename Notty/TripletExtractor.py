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
		att = subj = pred = {}
		att = self.extractAttribute()
		subj = self.extractSubject()
		pred = self.extractPredicate()
		obj = self.extractObject()
		# Handle Empty Sets
		if len(att)==0 or len(att)==0 or len(att)==0:
			return {}
		else:
			return att | subj | pred | obj

	def extractAttribute(self,tree):
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

	def extractObject(self,VP_sbtree):
		# siblings <- find NP, PP and ADJP siblings of VP_subtree 
		#siblings = 
		# for each value in siblings do 
			# if value = NP or PP 
				# object <- first noun in value
			# else
				# object <- first adjective in value
			# objectAttributes <- EXTRACT-ATTRIBUTES(object) 
		# result <- object | objectAttributes 
		# if result != failure then return result 
		# else return failure
		return {}

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
