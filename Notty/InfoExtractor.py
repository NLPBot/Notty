import nltk.data
import pickle
from gensim import corpora, models, similarities
from collections import defaultdict
from nltk.corpus import stopwords
from KnowledgeGraph import K_Graph

# A class that process raw search results &
# chooses valid information
class InfoExtractor(object):

	"""docstring for InfoExtractor"""
	def __init__(self, raw_output):
		super(InfoExtractor, self).__init__()
		self.raw_output = raw_output

	def getExtractedResults(self):
		# Process raw output, then return output
		sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
		sents = sent_detector.tokenize(self.raw_output.strip()) # return complete sentences
		# Select sentences
		return self.sentsSelector(sents)

	def removeStopWords(self,tokens):
		return [w for w in tokens if not w in stopwords.words('english')]

	def removeSingleOccurWords(self,tokens):
		frequency = defaultdict(int)
		for token in tokens:
			frequency[token] += 1
		return [token for token in tokens if frequency[token] > 1]

	def sentsSelector(self,sents):
		texts = []
		new_indices = []
		index = 0
		for sent in sents:
			tokens = sent.split()
			if len(self.removeSingleOccurWords(self.removeStopWords(tokens)))>0:
				texts.append(self.removeStopWords(tokens))
				new_indices.append(index)
				#print(self.removeSingleOccurWords(self.removeStopWords(tokens)))
			index += 1

		self.makeDictAndCorpus(texts)
		new_sents = []
		for index in self.DocumentSIMQuery():
			new_sents.append(sents[index])
		return new_sents

	def makeDictAndCorpus(self,texts):
		dictionary = corpora.Dictionary(texts)
		#print(dictionary.token2id)
		dictionary.save('/tmp/sim.dict')
		corpus = [dictionary.doc2bow(text) for text in texts]
		corpora.MmCorpus.serialize('/tmp/sim.mm', corpus) # store to disk, for later use

	def DocumentSIMQuery(self):
		dictionary = corpora.Dictionary.load('/tmp/sim.dict')
		corpus = corpora.MmCorpus('/tmp/sim.mm') 
		lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)

		# Set up single doc for query
		k_graph = K_Graph().load() # Obtain knowledge graph
		topic = k_graph.get_topic()
		#topic = 'The Qing dynasty of China later defeated the kingdom and annexed Taiwan.'
		vec_bow = dictionary.doc2bow(topic.lower().split())
		vec_lsi = lsi[vec_bow] # convert the query to LSI space

		# Initialize query structure
		index = similarities.MatrixSimilarity(lsi[corpus]) # transform corpus to LSI space and index it
		index.save('/tmp/sim.index')
		index = similarities.MatrixSimilarity.load('/tmp/sim.index')

		sims = index[vec_lsi] # perform a similarity query against the corpus
		#print(list(enumerate(sims))) # print (document_number, document_similarity) 2-tuples
		sims = sorted(enumerate(sims), key=lambda item: -item[1])
		print(sims) # print sorted (document number, similarity score) 2-tuples

		# Return Top five most semantically similar sentences
		indices = []
		count = 0
		for sim in sims:
			if count<5:
				indices.append(sim[0])
				count += 1
		return indices











