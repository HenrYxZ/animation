import cv2
import sys
import numpy as np

# ------------- CAMERA/PROJECTION PARAMETERS

focal_lenght = [3049.4772875915637, 3054.6162360490512]
principal_point = [1547.3066447988792, 994.90151571819047]


camera_matrix = np.matrix([[focal_lenght[0], 0., principal_point[0]], [0, focal_lenght[1], principal_point[1]], [0., 0., 1.]])

# Camera pose -> Y = 2.5cm, X = 0, 5.4, 10.8, 16.6 cm, Z = 0, Rotation = Identity

# Rotation and Translation matrices
# Left Image 
RT_1 = np.matrix([[1., 0., 0., 0.], [0., 1., 0., 2.5], [0., 0., 1.,0.]])
# Center Left Image
RT_2 = np.matrix([[1., 0., 0., 5.4], [0., 1., 0., 2.5], [0., 0., 1., 0.]])
# Center Right Image
RT_3 = np.matrix([[1., 0., 0., 10.8], [0., 1., 0., 2.5], [0., 0., 1., 0.]])
# Center Right Image
RT_4 = np.matrix([[1., 0., 0., 16.6], [0., 1., 0., 2.5], [0., 0., 1., 0.]])

# Projection matrices
P1 = camera_matrix * RT_1
P2 = camera_matrix * RT_2
P3 = camera_matrix * RT_3
P4 = camera_matrix * RT_4




# ----------- CORNERS ON IMAGES

corners_1 = []
# Point 1 on image1 (Left)
corners_1.append(np.array((2644., 220.)))
# Point 2 corner on image1 (Left)
corners_1.append(np.array((2116., 784.)))
# Point 3 corner on image1 (Left)
corners_1.append(np.array((3028., 952.)))
corners_1.append(np.array((1., 1.)))

corners_2 = []
# Point 1 corner on image2 (Center Left)
corners_2.append(np.array((2072., 192.)))
# Point 2 corner on image2 (Center Left)
corners_2.append(np.array((1526., 776.)))
# Point 3 corner on image2 (Center Left)
corners_2.append(np.array((2290., 940.)))
corners_2.append(np.array((1., 1.)))

# number of pixels in Y in the camera
max_y = 2303.

for point in corners_1:
	point[1] = max_y-point[1]

for point in corners_2:
	point[1] = max_y-point[1]

"""

for point in corners_3_l:
	point[1] = 2590-point[1]

for point in corners_3_r:
	point[1] = 2590-point[1]
"""

"""
corners_3_r = []
# Front Right corner on image3 (Center)
corners_3_r.append(np.array((1590., 2313.)))
# Back Right corner on image3 (Center)
corners_3_r.append(np.array((1446., 2020.)))

corners_3_l = []
# Front Left corner on image3 (Center)
corners_3_l.append(np.array((170., 2298.)))
# Back Left corner on image3 (Center)
corners_3_l.append(np.array((410., 2016.)))
"""


# --------------  PROJECTION MATRICES

# Homogeneous arrays
a3xN = np.array([[ corners_1[0][0],  corners_1[0][1]],
              [ corners_1[1][0],  corners_1[1][1]],
              [ corners_1[2][0],  corners_1[2][1]],
              [ 1.   ,  1.  ]])

b3xN = np.array([[ corners_2[0][0],  corners_2[0][1]],
              [ corners_2[1][0],  corners_2[1][1]],
              [ corners_2[2][0],  corners_2[2][1]],
              [ 1.   ,  1.  ]])

as3xN = np.array([[corners_1[0][0],  corners_1[1][0],   corners_1[2][0]],
                 [ corners_1[0][1],  corners_1[1][1],   corners_1[2][1]],
               	 [ 		     1.,  		    	1., 			 	1.]])

bs3xN = np.array([[corners_2[0][0],  corners_2[1][0],   corners_2[2][0]],
              	 [ corners_2[0][1],  corners_2[1][1],   corners_2[2][1]],
              	 [ 		     	1., 			  1.,				1.]])

"""
b3xN = np.array([[ corners_3_r[0][0],  corners_3_r[1][0]],
              [ corners_3_r[0][1],  corners_3_r[1][1]],
              [ 1.   ,  1.  ]])

d3xN = np.array([[ corners_3_l[0][0],  corners_3_l[1][0]],
              [ corners_3_l[0][1],  corners_3_l[1][1]],
              [ 1.   ,  1.  ]])
"""

p1 = cv2.triangulatePoints(P1[:3], P2[:3], as3xN[:2], bs3xN[:2])
# p2 = cv2.triangulatePoints(F2[:3], F3[:3], c3xN[:2], d3xN[:2])

p1 /= p1[3]
# p2 /= p2[3]

print "Puntos en la derecha"
print p1

"""
print "\n puntos en la izquierda"
print p2
"""