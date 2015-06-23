from TripletExtractor import TripletExtractor
from stat_parser import Parser
import copy
from nltk.corpus import stopwords
import wikipedia
import nltk

parser = Parser()
#summary = wikipedia.summary('taiwan')
#sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
#sents = sent_detector.tokenize(summary.strip())
tree_list = []
#for sent in sents[:4]:
#	print(sent)
#	tree_list.append(parser.parse(sent))
tree_list.append(parser.parse('I love you'))
tree_list.append(parser.parse('A rare black squirrel has become a regular visitor to a suburban garden.'))

### Test for TripletExtractor ###
for t in tree_list:
	print('-------------------------------------------------------------')
	print(str(t)+'\n\n')
	e = TripletExtractor(t)

	## Testing smaller submodules ##
	print(' getVPSubtree '+str(e.getVPSubtree())+'\n') # getVPSubtree
	print(' getVPSiblings '+str(e.getVPSiblings())+'\n') # getVPSiblings
	print(' getNPSubtree '+str(e.getNPSubtree())+'\n') # getNPSubtree
	#print(''+str(e.)) # getMANYSiblings
	#print(''+str(e.)) # getADVPSiblings
	#print(''+str(e.)) # getRBSiblings

	print(' getSiblings '+str(e.getSiblings(t,e.getNPSubtree()))) # getSiblings
	print(' getSiblings '+str(e.getSiblings(t,e.getVPSubtree()))) # getSiblings
		
	#print(''+str(e.)) # getUncles
	#print(''+str(e.)) # extractAttribute

	#print(''+str(e.)) # extractSubject
	#print(''+str(e.)) # extractPredicate
	#print(''+str(e.)) # extractObject

	#print('deepest verb is: ' + str(e.FindDeepestVerb(t,0).label())) # FindDeepestVerb
	#print(' First Noun is: ' + str(e.FindFirstNoun(t))) # FindFirstNoun
	print('-------------------------------------------------------------')

## Simple test for complete run ##
#e = TripletExtractor(parser.parse('I love you'))
#print(str(e.extract()))







