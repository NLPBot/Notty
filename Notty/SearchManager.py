from InfoAggregator import InfoAggregator
from InfoExtractor import InfoExtractor
from KnowledgeGraph import K_Graph
import pickle

class SearchManager(object):

	"""docstring for SearchManager"""
	def __init__(self, input):
		self.input = input

	# Return results in list of strings
	def getResults(self):
		# Determine search options and formats...
		infoAggregator = InfoAggregator(self.input)
		# Have loop that determines when search terminates
		raw_output = infoAggregator.getRawResults()
		infoExtractor = InfoExtractor(raw_output)
		# Obtain knowledge graph
		k_graph = K_Graph().load()
		# Add all sentences
		for sent in infoExtractor.getExtractedResults():
			k_graph.add_point(self.input,sent)
		k_graph.save()

