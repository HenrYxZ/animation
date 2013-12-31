import cv2
import sys
import numpy as np
from color_test import find_points
import math

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

# ------------------ INFORMACION USADA EN EL TEST -----------------------------

# Cantidad de puntos que vamos a buscar
NUMBER_OF_POINTS = 5

# Alto de la imagen para traspasar el eje y positivo hacia arriba
IMAGE_HEIGHT = 720

# Obtener las matrices de calibracion de las dos camaras

# Webcam
focal_lenght_1 = [ 1169.714437664702900, 1171.172019048536200 ]
principal_point_1 = [ 667.264086590390550, IMAGE_HEIGHT - 360.838874317338880 ]

# Celular
focal_lenght_2 = [ 1143.746397921609100, 1150.900867474856800 ]
principal_point_2 = [ 644.388054840155970, IMAGE_HEIGHT - 289.264135801620970 ]

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

first_points_1 = [[609., IMAGE_HEIGHT - 198.],
				  [672., IMAGE_HEIGHT - 180.],
				  [732., IMAGE_HEIGHT - 195.],
				  [669., IMAGE_HEIGHT - 222.],
				  [666., IMAGE_HEIGHT - 252.]]

first_points_2 = [[180., IMAGE_HEIGHT - 213.],
 				  [324., IMAGE_HEIGHT - 189.],
 				  [411., IMAGE_HEIGHT - 219.],
 				  [324., IMAGE_HEIGHT - 249.],
 				  [324., IMAGE_HEIGHT - 282.]]

# ------------------------- PRINCIPIO DEL PROGRAMA ---------------------------

# ------------- FUNCIONES AUXILIARES -------------
def get_camera_matrix(focal_lenght, principal_point):
	# Numpy intrinsic matrix
	camera_matrix =  np.matrix([[focal_lenght[0], 0., principal_point[0]],
 		[0, focal_lenght[1], principal_point[1]], [0., 0., 1.]])
	return camera_matrix


# Funcion auxiliar para imprimir un punto 2D
def point2d_to_str(point):
	s_x = "x = " + str(point[0])
	s_y = " y = " + str(point[1]) + "\n"
	s = s_x + s_y
	return s

def point3d_to_str(point):
	s_x = str(point[0]) + ", "
	# Esto se hace porque por alguna razon Y sale negativo
	if point[1] < 0:
		point[1] *= -1
	s_y = str(point[1]) + ", "
	s_z = str(point[2]) + ",\n"
	s = s_x + s_y + s_z
	return s

def find_closest(point, set):
	# Cambiar min_dist para imagenes de altisima resolucion
	min_dist = 100000
	answer = 0
	for p in set:
		dist = math.sqrt((p[0]-point[0])**2 + (p[1]-point[1])**2)
		if dist < min_dist:
			min_dist = dist
			answer = p
	return answer

def find_all_icp(previus_points, points):
	answer = []
	aux = points
	for p in previus_points:
		closest = find_closest(p, aux)
		aux.remove(closest)
		answer.append(closest)
	return answer

def draw_circles(img, points):
	for p in points:
		cv2.circle(img, (int(p[0]), int(p[1])), 5, 255, -1)


# ----------- FUNCIONES PRINCIPALES ---------------------

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
def process_videos(cap_1, cap_2, P1, P2, first_points_1, first_points_2):
	'''
	Se necesitan dos capturas de video y las dos matrices de proyeccion
	correspondientes, ademas los puntos 2D en la primera imagen para seguirlos
	con el algoritmo Iterative Closest Point con esto se escriben los logs que
	tienen la informacion de los puntos encontrados
	'''
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

		# Los puntos 2D encontrados a mano solo en la primera imagen
		if counter == 0:
			prev_points_1 = first_points_1
			prev_points_2 = first_points_2
			

		# Encontrar puntos en ambos conjuntos
		first_camera_points = set(find_points(img_1, 1, IMAGE_HEIGHT))
		second_camera_points = set(find_points(img_2, 2, IMAGE_HEIGHT))

		# Escribir estos puntos 2D encontrados

		header = "New frame number :" + str(counter) + "\n"
		log_1.write(header)
		log_2.write(header)

		for point in first_camera_points:
			s = point2d_to_str(point)
			log_1.write(s)

		for point in second_camera_points:
			s = point2d_to_str(point)
			log_2.write(s)


		# ------- Si se estan sacando menos puntos de los debidos no hacer nada

		if (len(first_camera_points) >= NUMBER_OF_POINTS) and (len(second_camera_points) >= NUMBER_OF_POINTS):

			# Ordenar puntos para que queden los correspondientes en la otra camara de cada imagen

			# Se buscan los puntos de forma iterativa, pensando que no se mueven mucho
			# con respecto al frame anterior, con los puntos ordenados (Algoritmo ICP)
			first_cam_points = list(first_camera_points)
			second_cam_points = list(second_camera_points)

			'''	
			for point in first_cam_points:
				point = point + (1.,)
			for point in second_cam_points:
				point = point + (1.,)
			'''

			first_cam_points.sort()
			second_cam_points.sort()

			first_cam_points = find_all_icp(prev_points_1, first_cam_points)
			second_cam_points = find_all_icp(prev_points_2, second_cam_points)

			# actualizar los puntos 2D para que se encuentren los mas parecidos
			# en la siguiente iteracion
			prev_points_1 = first_cam_points
			prev_points_2 = second_cam_points

			# Escribir copia de imagen con los puntos encontrados cada 20 frames

			if (counter % 20 == 0):
				draw_circles(img_1, first_cam_points)
				draw_circles(img_2, second_cam_points)
				cv2.imwrite('imgs/first/first_{0:05d}.jpg'.format(counter),img_1)
				cv2.imwrite('imgs/second/second_{0:05d}.jpg'.format(counter),img_2)

			a3xN = np.transpose( np.array(first_cam_points) )
			b3xN = np.transpose( np.array(second_cam_points) )

			print "a "
			print a3xN
			print "b "
			print b3xN

			# Triangular cada punto en el arreglo de puntos de cada imagen

			points = cv2.triangulatePoints(P1[:3], P2[:3], a3xN[:2], b3xN[:2])
			points /= points[3]

			# matriz de los puntos
			mat_points = np.transpose(points)
			print mat_points

			# Escribir esto a un archivo
			header = "New frame number :" + str(counter) + "\n"
			log.write(header)

			for point in mat_points:
				s = point3d_to_str(point)
				log.write(s)

		counter += 1

	# Fin del while
	log.close()
	log_1.close()
	log_2.close()


# --------------------- El main ----------------------
if __name__ == "__main__":

	print ("Path for first camera video\n")
	# source_1 = raw_input()
	source_1 = "../../facial_capture_videos/tres_webcam.mp4"
	print ("Path for second camera video\n")
	# source_2 = raw_input()
	source_2 = "../../facial_capture_videos/tres_cel.mp4"


	# Matrices de Proyeccion
	# La matriz de proyeccion es multiplicada por la identidad porque se supone en
	# el origen del sistema de coordenadas 3D
	first_camera_matrix = get_camera_matrix(focal_lenght_1, principal_point_1)
	second_camera_matrix = get_camera_matrix(focal_lenght_2, principal_point_2)

	first_projection_matrix = first_camera_matrix * RT_1
	second_projection_matrix = second_camera_matrix * RT_2

	cap_1, cap_2 = get_videos(source_1, source_2)
	process_videos(cap_1, cap_2, first_projection_matrix,
		second_projection_matrix, first_points_1, first_points_2)
	# Cerrar todo
	cv2.destroyAllWindows()

