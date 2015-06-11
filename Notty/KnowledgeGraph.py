from ete2 import Tree
import pickle

# Class that builds knowledge graph
# Allows addition & deletion of nodes
# Strictly tree operation
class K_Graph(object):

	"""docstring for K_Graph"""
	def __init__(self):
		self.theme = Tree()
		self.topic = ''

	def add_point(self,topic,point):
		for t in self.theme.traverse():
			if t.name in topic:
				t.add_child(name=point)

	def add_topic(self,topic):
		self.theme.add_child(name=topic)
		self.topic = topic

	def getCurrentGraph(self):
		for t in self.theme.traverse():
			if t.name in self.topic:
				return t

	def get_topic(self):
		return self.topic

	def save(self):
		with open('data.pickle', 'wb') as f: 
			# Pickle the 'data' dictionary using the highest protocol available. 
			pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

	def load(self):
		with open('data.pickle', 'rb') as f: 
			# The protocol version used is detected automatically, so we do not # have to specify it. 
			return pickle.load(f)