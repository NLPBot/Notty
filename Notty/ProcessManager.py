from SlideManager import SlideManager
from KnowledgeGraph import K_Graph
import pickle

# Process initial process and create slides #
class ProcessManager(object):

	"""docstring for ProcessManager"""
	def __init__(self,raw_input):
		super(ProcessManager, self).__init__()
		# Make input processing decisions
		self.valid_raw_input = raw_input

	def setSlideElements(self):
		self.init(self.valid_raw_input)

	# Unwrap knowledge graph, return tuples (level,text)
	def getSlideElements(self):
		# Obtain knowledge graph
		k_graph = K_Graph().load()
		topic = k_graph.getCurrentGraph()
		# unwrap and create (level,text) tuples
		level = 0
		tuples = []
		# Traverse
		#level += 1
		for point in topic.get_children():
			if point.name not in k_graph.get_topic():
				tuples.append((level,point.name))
		return tuples

	# Make and return a slide
	def init(self,valid_raw_input):
		slideManager = SlideManager(valid_raw_input)
		slideManager.makeSlideElements()
