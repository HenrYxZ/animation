'''
Parser for the log.txt, reads the frames and points and
gives a list of frames, each frame with a set of points

Created on December 25 2013
@author: Hernaldo Henriquez
'''

from frame import Frame
from geom import Vector3

def parse(file_name, num_of_points):

	frames = []
	f = open(file_name)

	while(True):
		line = f.readline()
		if (line==-1 or line==""):
			break

		frame_num = int((line.split(":"))[1])
		frame = Frame(frame_num)

		for i in range(num_of_points):
			line = f.readline()
			positions = line.split(",")
			x = float(positions[0].strip())
			y = float(positions[1].strip())
			z = float(positions[2].strip())
			p = Vector3(x, y, z)
			frame.points.append(p)

		frames.append(frame)

	return frames


