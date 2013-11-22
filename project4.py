import cv2
import sys
import numpy as np
from color_test import find_points

global first_camera_points
first_camera_points = []
global second_camera_points
second_camera_points = []

global first_video
global second_video

global first_camera_matrix
global second_camera_matrix

global first_projection_matrix
global second_projection_matrix

# Los puntos en tres dimensiones
global points

# Obtener las matrices de calibracion de las dos camaras

# Obtener dos videos
def get_videos(source_1, source_2):
	first_cap = cv2.VideoCapture(source_1)
	second_cap = cv2.VideoCapture(source_2)

	if first_cap is None or not first_cap.isOpened():
        print 'Warning: unable to open video source: ', source_1
    if second_cap is None or not second_cap.isOpened():
        print 'Warning: unable to open video source: ', source_2

    return first_cap, second_cap

	# Transformar a dos conjuntos de imagenes
def process_videos(cap_1, cap_2):

	log = open("log.txt", "w")
	log_1 = open("log_1.txt", "w")
	log_2 = open("log_2.txt", "w")

	counter = 0

	while True:
		ret_1, img_1 = first_cap.read()
		ret_2, img_2 = second_cap.read()
		# Si se acabo uno de los videos
		if not ret_1 or not ret_2:
			break

		counter += 1
		# Encontrar puntos en ambos conjuntos
		first_camera_points = find_points(img_1)
		second_camera_points = find_points(img_2)

		# Ordenar puntos para que queden los correspondientes en la otra camara de cada imagen

		'''
		muy peludo
		'''

		# Triangular cada punto en el arreglo de puntos de cada imagen

		a3xN = first_camera_points.append(np.array(1, 1))
		b3xN = second_camera_points.append(np.array(1, 1))

		points = cv2.triangulatePoints(first_projection_matrix[:3], 
			second_projection_matrix[:3], a3xN[:2], b3xN[:2])
		points /= points[3]

		# Escribir esto a un archivo
		header = "New frame number " + str(counter) + ": \n"
		log.write(header)

		for point in points:
			s_x = "x = " + str(point[0])
			s_y = " y = " + str(point[1])
			s_z = " z = " + str(point[2]) + "\n"
			s = s_x + s_y + s_z
			log.write(s)

# Cerrar todo
cv2.destroyAllWindows()