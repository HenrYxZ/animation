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

# Cantidad de puntos que vamos a buscar
NUMBER_OF_POINTS = 5

# Obtener las matrices de calibracion de las dos camaras

	# Webcam
focal_lenght_1 = [ 1169.714437664702900, 1171.172019048536200 ]
principal_point_1 = [ 667.264086590390550, 360.838874317338880 ]

first_camera_matrix = np.matrix([[focal_lenght_1[0], 0., principal_point_1[0]],
 [0, focal_lenght_1[1], principal_point_1[1]], [0., 0., 1.]])

	# Celular
focal_lenght_2 = [ 1143.746397921609100, 1150.900867474856800 ]
principal_point_2 = [ 644.388054840155970, 289.264135801620970 ]

second_camera_matrix = np.matrix([[focal_lenght_2[0], 0., principal_point_2[0]],
 [0, focal_lenght_2[1], principal_point_2[1]], [0., 0., 1.]])

# Rotation and Translation matrices
# Matriz fundamental para pasar de la camara uno a la dos (se supone ausencia
#	de rotaciones)
# Distancia entre camaras medida con regla (cms)
translation_x = -19.1
translation_y = 5.8
translation_z = 4.4
RT_1 = np.matrix([[1., 0., 0., 0], 
				  [0., 1., 0., 0],
				  [0., 0., 1., 0]])
RT_2 = np.matrix([[1., 0., 0., translation_x], 
				  [0., 1., 0., translation_y],
				  [0., 0., 1., translation_z]])


# Matrices de Proyeccion
# La matriz de proyeccion es multiplicada por la identidad porque se supone en
# el origen del sistema de coordenadas 3D
first_projection_matrix = first_camera_matrix * RT_1
second_projection_matrix = second_camera_matrix * RT_2

# Funcion auxiliar para imprimir un punto 2D
def print_point2d(point):
	s_x = "x = " + str(point[0])
	s_y = " y = " + str(point[1]) + "\n"
	s = s_x + s_y
	return s

# Obtener dos videos
def get_videos(source_1, source_2):
	first_cap = cv2.VideoCapture(source_1)
	second_cap = cv2.VideoCapture(source_2)

	if (first_cap is None) or (not first_cap.isOpened()):
		print('Warning: unable to open video source: ' +  source_1)
	if (second_cap is None) or (not second_cap.isOpened()):
		print('Warning: unable to open video source: ' + source_2)

	return first_cap, second_cap

	# Transformar a dos conjuntos de imagenes
def process_videos(cap_1, cap_2):

	log = open("log.txt", "w")
	log_1 = open("log_1.txt", "w")
	log_2 = open("log_2.txt", "w")

	counter = 0

	while True:
		ret_1, img_1 = cap_1.read()
		ret_2, img_2 = cap_2.read()
		# Si se acabo uno de los videos
		if not ret_1 or not ret_2:
			break

		counter += 1
		# Encontrar puntos en ambos conjuntos
		first_camera_points = set(find_points(img_1, 1))
		second_camera_points = set(find_points(img_2, 2))

		# Escribir estos puntos 2D encontrados

		header = "New frame number " + str(counter) + ": \n"
		log_1.write(header)
		log_2.write(header)

		for point in first_camera_points:
			s = print_point2d(point)
			log_1.write(s)

		for point in second_camera_points:
			s = print_point2d(point)
			log_2.write(s)

		# Ordenar puntos para que queden los correspondientes en la otra camara de cada imagen

		'''
		muy peludo
		'''

		# Si se estan sacando mas puntos de los debidos no hacer nada

		if (len(first_camera_points) == NUMBER_OF_POINTS) and (len(second_camera_points) == NUMBER_OF_POINTS):


			# Triangular cada punto en el arreglo de puntos de cada imagen

			first_cam_points = list(first_camera_points)
			second_cam_points = list(second_camera_points)
			for point in first_cam_points:
				point = point + (1.,)
			for point in second_cam_points:
				point = point + (1.,)

			a3xN = np.transpose( np.array(first_cam_points) )
			b3xN = np.transpose( np.array(second_cam_points) )

			print "a "
			print a3xN
			print "\n b "
			print b3xN

			points = cv2.triangulatePoints(first_projection_matrix[:3], second_projection_matrix[:3], a3xN[:2], b3xN[:2])
			points /= points[3]

			# matriz de los puntos
			mat_points = np.transpose(points)
			print mat_points

			# Escribir esto a un archivo
			header = "New frame number " + str(counter) + ": \n"
			log.write(header)

			for point in mat_points:
				s_x = "x = " + str(point[0])
				s_y = " y = " + str(point[1])
				s_z = " z = " + str(point[2]) + "\n"
				s = s_x + s_y + s_z
				log.write(s)

	# Fin del while
	log.close()
	log_1.close()
	log_2.close()


# --------------------- El main ----------------------
if __name__ == "__main__":

	print ("Path for first camera video\n")
	source_1 = raw_input()
	print ("Path for second camera video\n")
	source_2 = raw_input()

	cap_1, cap_2 = get_videos(source_1, source_2)
	process_videos(cap_1, cap_2)
	# Cerrar todo
	cv2.destroyAllWindows()

