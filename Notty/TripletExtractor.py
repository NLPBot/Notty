from nltk.tree import *
from sets import Set

class TripletExtractor(object):
	"""docstring for TripletExtractor"""
	def __init__(self, tree):
		self.tree = tree
		self.max_level = 0
		self.deepest_verb = None
	
	# Return a set consisting of triplet [ subj, pred, obj ]
	def extract(self):
		#print(' WITHIN extract ...... ')

		# First get all the sets
		att = subj = pred = obj = []
		subj = self.extractSubject(self.getNPSubtree())
		pred = self.extractPredicate(self.getVPSubtree())
		for VPSibling in self.getVPSiblings():
			if len(VPSibling)>0:
				obj.extend(self.extractObject(VPSibling))
		# Handle Empty Sets
		if subj==None or pred==None or obj==None:
			return []
		if len(subj)==0: 
			return []
		elif len(pred)==0:
			return [] 
		elif len(obj)==0:
			return []
		else:
			return ((att.extend(subj)).extend(pred)).extend(obj)

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
			result.extend(self.getRBSiblings(siblings)[0])
		# else
		else:
			# if noun(word) 
			if 'N' in word.label():
				# result <- all DT, PRP$, POS, JJ, CD, ADJP, QP, NP siblings
				result.extend(self.getMANYSiblings(siblings))
			# else
			else:
				# if verb(word)
				if 'V' in word.label(): 
					# result <- all ADVP siblings
					result.extend(self.getADVPSiblings(siblings))

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
		result = subject = []
		if self.FindFirstNoun(subtree)==None:
			return result
		else:
			subject.append(self.FindFirstNoun(subtree))
		# subjectAttributes <- EXTRACT-ATTRIBUTES(subject) 
		subjectAttributes = self.extractAttribute(subtree)
		# result <- subject | subjectAttributes
		result = subject.extend(subjectAttributes)
		# if result != failure then return result 
		# else return failure
		return result

	def extractPredicate(self,VP_subtree):
		#print(' WITHIN extractPredicate ...... ')

		# predicate <- deepest verb found in VP_subtree 
		predicate = self.FindDeepestVerb(VP_subtree,0)
		# predicateAttributes <- EXTRACT-ATTRIBUTES(predicate) 
		predicateAttributes = self.extractAttribute(predicate)
		# result <- predicate | predicateAttributes 
		result = predicate.extend(predicateAttributes)
		# if result != failure then return result 
		# else return failure 
		return result

	def extractObject(self,VP_sbtree):
		#print(' WITHIN extractObject ...... ' + str(VP_sbtree))

		siblings = self.getSiblings(self.tree,VP_sbtree)
		# siblings <- find NP, PP and ADJP siblings of VP_subtree 
		# for each value in siblings do 
		result = []
		object = None
		for value in siblings:
			value_label = value.label()
			# if value = NP or PP 
			if 'NP' in value_label or 'PP' in value_label:
				# object <- first noun in value
				if len(self.FindFirstNoun(value))>0:
					object = self.FindFirstNoun(value)[0]
			# else
			if 'JJ' in value_label:
				# object <- first adjective in value
				object = value
			# objectAttributes <- EXTRACT-ATTRIBUTES(object) 
			objectAttributes = self.extractAttribute(object)
		# result <- object | objectAttributes 
		if object==None:
			return result
		else:
			result = [object].extend(objectAttributes)

	def getUncles(self,tree,target):
		#print(' WITHIN getUncles ...... ')

		uncles = []
		if len(tree)==1:
			return uncles
		found = False
		for child in tree:
			if target.label() in child.label():
				found = True
				break
			uncles.extend(self.getUncles(child,target))
		if found == True:
			uncles = self.getSiblings(self.tree,tree)
		return uncles

	def getSiblings(self,tree,target):
		print(' WITHIN getSiblings ...... ')
		siblings = []
		if (tree.height())==2:
			return siblings
		found = False
		for child in tree:
			try:
				if str(target.label()) == str(child.label()):
					found = True
					break
			except AttributeError:
				print('AttributeError!')
				return siblings
			siblings.extend(self.getSiblings(child,target))
		if found == True:
			for child in tree:
				siblings.append(child)
		return siblings

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
		for sibling in siblings.subtrees():
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

		first_noun = []
		NP_tree = None
		for child in subtree:
			if 'NP' in child.label(): 
				NP_tree = child
		if NP_tree is not None:
			for n in NP_tree:
				if 'NN' in n.label():
					first_noun.append(n)
		return first_noun

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
