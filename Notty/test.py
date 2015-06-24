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
#tree_list.append(parser.parse('I love you'))
#tree_list.append(parser.parse('A rare black squirrel has become a regular visitor to a suburban garden.'))
#tree_list.append(parser.parse('Moreover, for each element composing the triplet, we find its attributes'))
#tree_list.append(parser.parse('In the past couple of decades the tide has changed somewhat as we moved to an information economy rather than an industrial one.'))

### Test for TripletExtractor ###
for t in tree_list:
	print('-------------------------------------------------------------')
	print(str(t)+'\n\n')
	e = TripletExtractor(t)

	## Testing smaller submodules ##
	#print(' getVPSubtree '+str(e.getVPSubtree())+'\n') # getVPSubtree
	#print(' getVPSiblings '+str(e.getVPSiblings())+'\n') # getVPSiblings
	#print(' getNPSubtree '+str(e.getNPSubtree())+'\n') # getNPSubtree
	#print(' getMANYSiblings '+str(e.getMANYSiblings(e.getSiblings(t,e.getNPSubtree())))) # getMANYSiblings
	#print(' getADVPSiblings '+str(e.getADVPSiblings(e.getSiblings(t,e.getNPSubtree())))) # getADVPSiblings
	#print(' getRBSiblings '+str(e.getRBSiblings(e.getSiblings(t,e.getNPSubtree())))) # getRBSiblings


	#print(' getSiblings of '+str(e.getNPSubtree())+'   '+str(e.getSiblings(t,e.getNPSubtree()))) # getSiblings
	#print(' getSiblings of '+str(e.getVPSubtree())+'   '+str(e.getSiblings(t,e.getVPSubtree()))) # getSiblings		
	#for uncle in e.getUncles(t,e.FindFirstNoun(t)):	# getUncles
	#	print(' uncles are \n' + str(uncle) + '\n')

	#print(''+str(e.extractAttribute(e.getNPSubtree()))) # extractAttribute

	print(' extractSubject '+str(e.extractSubject(e.getNPSubtree()))) # extractSubject
	print(' extractPredicate '+str(e.extractPredicate(e.getVPSubtree()))) # extractPredicate
	print(' extractObject '+str(e.extractObject())) # extractObject

	#print('deepest verb is: ' + str(e.FindDeepestVerb(t,0).label())) # FindDeepestVerb
	#print(' First Noun is: ' + str(e.FindFirstNoun(t))) # FindFirstNoun
	print('-------------------------------------------------------------')

## Simple test for complete run ##
#e = TripletExtractor(parser.parse('I love you'))
#print(str(e.extract()))







