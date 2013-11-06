import cv2
import sys
import numpy as np


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

# Transformar a dos conjuntos de imagenes

# Encontrar puntos en ambos conjuntos

# Ordenar puntos para que queden los correspondientes en la otra camara de cada imagen

# Triangular cada punto en el arreglo de puntos de cada imagen

a3xN = first_camera_points.append([1., 1.])
b3xN = second_camera_points.append([1., 1.])

points = cv2.triangulatePoints(first_projection_matrix[:3], second_projection_matrix[:3], a3xN[:2], b3xN[:2])

# Escribir esto a un archivo
