from SearchManager import SearchManager
from LayoutManager import LayoutManager
from KnowledgeGraph import K_Graph
import pickle

class ContentManager(object):

	"""docstring for ContentManager"""
	def __init__(self, input):
		super(ContentManager, self).__init__()
		self.input = input

	# Return search option and search contents
	def getContentUnits(self):
		# Obtain knowledge graph
		k_graph = K_Graph().load()
		k_graph.add_topic(self.input)
		k_graph.save()
		# Expand graph
		searchManager = SearchManager(self.input)
		layoutManager = LayoutManager(searchManager.getResults())
