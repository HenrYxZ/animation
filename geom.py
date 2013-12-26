class Point3:

	def __init__(self, x=0., y=0., z=0.):
		self._x = x
		self._y = y
		self._z = z

	@property
	def x(self):
	    return self._x
	@x.setter
	def x(self, value):
	    self._x = value

	@property
	def y(self):
	    return self._y
	@y.setter
	def y(self, value):
	    self._y = value

	@property
	def z(self):
	    return self._z
	@z.setter
	def z(self, value):
	    self._z = value
	
	

def sumOfPoints(p1, p2):

	answer = Point3()
	answer.x = p1.x + p2.x
	answer.y = p1.y + p2.y
	answer.z = p1.z + p2.z
	return answer

def subOfPoints(p1, p2):

	answer = Point3()
	answer.x = p1.x - p2.x
	answer.y = p1.y - p2.y
	answer.z = p1.z - p2.z
	return answer

def scalarProd(p1,p2, scalar):

	answer = Point3()
	answer.x = (p1.x - p2.x) * scalar
	answer.y = (p1.y - p2.y) * scalar
	answer.z = (p1.z - p2.z) * scalar
	return answer

def projection(p1, p2, dimension):
	# The projection in one dimension for the vector made by p1 - p2
	if dimension == 'x':
		answer = Point3(0., p1.y - p2.y, p1.z - p2.z)
	elif dimension == 'y':
		answer = Point3(p1.x - p2.x, 0., p1.z - p2.z)
	elif dimension == 'z':
		answer = Point3(p1.x - p2.x, p1.y - p2.y, 0.)
	elif dimension == 'xy':
		answer = Point3(0., 0., p1.z - p2.z)
	elif dimension == 'xz':
		answer = Point3(0., p1.y - p2.y, 0.)
	else:
		answer = Point3(p1.x - p2.x, 0., 0.)
	return answer

class BoundingBox:

	def __init__(self, minPoint, maxPoint):
		self.minPoint = minPoint
		self.maxPoint = maxPoint

	def setMin(p):
		self.minPoint = p

	def setMax(p):
		self.maxPoint = p

	def getMin():
		self.minPoint

	def getMax():
		self.maxPoint