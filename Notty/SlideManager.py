from ContentManager import ContentManager
import pickle

# Manage Slide components # 

class SlideManager(object):
	"""docstring for SlideManager"""
	def __init__(self, valid_raw_input):
		super(SlideManager, self).__init__()
		self.input = valid_raw_input

	# Return a slide (body of texts)
	def makeSlideElements(self):
		self.getContentUnits()

	def getContentUnits(self):
		contenManager = ContentManager(self.input)
		contenManager.getContentUnits()
