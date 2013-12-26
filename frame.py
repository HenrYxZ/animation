'''
Frame class that contains the list of 3d points found

Created on December 25 2013
@author: Hernaldo Henriquez
'''

class Frame:
	def __init__(self, number, points = None):
		self._number = number
		self._points = points

	@property
	def number(self):
	    return self._number
	@number.setter
	def number(self, value):
	    self._number = value

	@property
	def points(self):
	    return self._points
	@points.setter
	def points(self, value):
	    self._points = value
	
	


