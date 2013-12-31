class Vector3:

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
	
def makeBB(vectors):

	max_x = 0
	max_y = 0
	max_z = 0

	min_x = 0
	min_y = 0
	min_z = 0

	for v in vectors:
		if (v.x > max_x):
			max_x = x
		if (v.y > max_y):
			max_y = y
		if (v.z > max_z):
			max_z = z

		if (v.x < min_x):
			min_x = x
		if (v.y < min_y):
			min_y = y
		if (v.z < min_z):
			min_z = z

	max_v = Vector3(max_x, max_y, max_z)
	min_v = Vector3(min_x, min_y, min_z)

	bb = BoundingBox(min_v, max_v)

	return bb

def sumOfVectors(p1, p2):

	answer = Vector3()
	answer.x = p1.x + p2.x
	answer.y = p1.y + p2.y
	answer.z = p1.z + p2.z
	return answer

def subOfVectors(p1, p2):

	answer = Vector3()
	answer.x = p1.x - p2.x
	answer.y = p1.y - p2.y
	answer.z = p1.z - p2.z
	return answer

def scalarProd(p1,p2, scalar):

	answer = Vector3()
	answer.x = (p1.x - p2.x) * scalar
	answer.y = (p1.y - p2.y) * scalar
	answer.z = (p1.z - p2.z) * scalar
	return answer

def projection(p1, p2, dimension):
	# The projection in one dimension for the vector made by p1 - p2
	answer = Vector3(0., 0., 0.)
	if dimension == 'x':
		answer = Vector3(0., p1.y - p2.y, p1.z - p2.z)
	elif dimension == 'y':
		answer = Vector3(p1.x - p2.x, 0., p1.z - p2.z)
	elif dimension == 'z':
		answer = Vector3(p1.x - p2.x, p1.y - p2.y, 0.)
	elif dimension == 'xy':
		answer = Vector3(0., 0., p1.z - p2.z)
	elif dimension == 'xz':
		answer = Vector3(0., p1.y - p2.y, 0.)
	else:
		answer = Vector3(p1.x - p2.x, 0., 0.)
	return answer

class BoundingBox:

	def __init__(self, minPoint, maxPoint):
		self._minPoint = minPoint
		self._maxPoint = maxPoint

	@property
	def minPoint(self):
	    return self._minPoint
	@minPoint.setter
	def minPoint(self, value):
	    self._minPoint = value

	@property
	def maxPoint(self):
	    return self._maxPoint
	@maxPoint.setter
	def maxPoint(self, value):
	    self._maxPoint = value
	
	