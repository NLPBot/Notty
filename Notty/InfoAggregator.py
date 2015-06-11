import wikipedia

class InfoAggregator(object):
	"""docstring for InfoAggregator"""
	def __init__(self, input):
		super(InfoAggregator, self).__init__()
		# Search input will be defined: 
		# 0 -> key word / phrases 
		# 1 -> Q & A
		self.search_option = 0
		self.search_input = input

	def getRawResults(self):
		# Make requests to wikipedia
		summary = wikipedia.summary(self.search_input)
		return summary
