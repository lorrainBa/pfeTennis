from PIL import Image, ImageDraw
from typing import Dict, Tuple
import numpy as np
import cv2
import time
from scipy.spatial import KDTree

global_rectangle_width = 200
global_rectangle_height = 432
# Fonction pour vérifier si un point est à l'intérieur du trapèze
def point_in_trapezoid(x, y, vertices):
    x0, y0 = vertices[0]
    x1, y1 = vertices[1]
    x2, y2 = vertices[2]
    x3, y3 = vertices[3]

    # Vérifie si le point est à l'intérieur des 4 côtés du trapèze
    if (y - y0) * (x1 - x0) - (x - x0) * (y1 - y0) > 0: return False
    if (y - y2) * (x3 - x2) - (x - x2) * (y3 - y2) > 0: return False
    if (y - y0) * (x3 - x0) - (x - x0) * (y3 - y0) < 0: return False
    if (y - y1) * (x2 - x1) - (x - x1) * (y2 - y1) < 0: return False
    
    return True


def associateTrapezoidToRectangle(trapezoidCoord,rectangleWidth = global_rectangle_width,rectangleHeight=global_rectangle_height):
    startLeftTop = trapezoidCoord["top_left"][0]
    startRightTop = trapezoidCoord["top_right"][0]
    smallTopWidth = startRightTop - startLeftTop
    
    hugeBotWidth = (trapezoidCoord["bottom_right"][0] - trapezoidCoord["bottom_left"][0])
    heightTrapez = trapezoidCoord["bottom_right"][1]
    coordCorrespondanceY = np.linspace(1, heightTrapez, rectangleHeight)

    #Calcul agrandissement de la largeur du terrain
    coefAgrandissementLargeur = hugeBotWidth/smallTopWidth
    # Créer une liste des coefficients d'agrandissement du terrain a chaque iteration en supossant que c'est linéaire
    coefByIteration = np.linspace(1, coefAgrandissementLargeur, rectangleHeight)

    dictionnaryCoords = {}
    allAnnotedCoords = []
    # On itere sur la hauteur du trapeze
    for i in range (rectangleHeight):
        currentAgrandissementCoeff = coefByIteration[i]
        currentHeight = coordCorrespondanceY[i]

        augmentationSize = int((smallTopWidth * currentAgrandissementCoeff - smallTopWidth)/2)
        currentLeft = startLeftTop - augmentationSize
        currentRight = startRightTop + augmentationSize

    
    

        coordCorrespondanceX = np.linspace(currentLeft, currentRight, rectangleWidth)

        for indexI,xCoordinate in enumerate(coordCorrespondanceX) :
            coordToAdd = (int(xCoordinate), int(currentHeight))
            dictionnaryCoords[coordToAdd] = indexI,i
            allAnnotedCoords.append(coordToAdd)
    return(dictionnaryCoords,allAnnotedCoords)






def coordonnee_plus_proche_kd(coord_entree, tree,liste_coordonnees):
    """Trouve la coordonnée la plus proche dans l'arbre KD."""
    dist, index = tree.query(coord_entree)
    return liste_coordonnees[index]




def colorier_zone_autour(image, coord_x, coord_y, couleur, taille_zone):
    """Colorie une zone autour d'une coordonnée dans une image avec une certaine couleur."""
    hauteur, largeur, _ = image.shape
    
    # Déterminer les limites de la zone à colorier
    debut_x = max(0, coord_x - taille_zone)
    fin_x = min(largeur - 1, coord_x + taille_zone)
    debut_y = max(0, coord_y - taille_zone)
    fin_y = min(hauteur - 1, coord_y + taille_zone)
    
    # Colorier chaque pixel dans la zone
    for y in range(debut_y, fin_y + 1):
        for x in range(debut_x, fin_x + 1):
            
            image[y, x] = couleur




def colorierPil(image, coord_x, coord_y, couleur, taille_zone):
    """Colorie une zone autour d'une coordonnée dans une image avec une certaine couleur."""
    hauteur, largeur = image.size
    
    # Déterminer les limites de la zone à colorier
    debut_x = max(0, coord_x - taille_zone)
    fin_x = min(largeur - 1, coord_x + taille_zone)
    debut_y = max(0, coord_y - taille_zone)
    fin_y = min(hauteur - 1, coord_y + taille_zone)

    # Colorier chaque pixel dans la zone
    for y in range(debut_y, fin_y + 1):
        for x in range(debut_x, fin_x + 1):
            image.putpixel((y,x), couleur)





#print(allAnnotedCoords)
# 200 432
def processFieldAndCoordonate(angleTrapez,rectangleWidth = global_rectangle_width,rectangleHeight=global_rectangle_height):
    
    # Determine precision of the point, with a factor of 2.16 to respect a tennis field
    
    # Get the dictionnary with, key = coord of the field, value = coord on the rectangle
    dictionnaryCoords,allAnnotedCoords = associateTrapezoidToRectangle(angleTrapez, rectangleWidth, rectangleHeight)
    #print(dictionnaryCoords)
    # Create a tree of the coords so it's easier to go through and find easily the nearest coord
    treeCoords = KDTree(allAnnotedCoords)

    """# Create a picture of the field with the point that detect impact
    image = np.zeros((1800, 1800, 3), dtype=np.uint8)

    # Draw red pixel on those coords
    for key in dictionnaryCoords:
        y, x = key
        image[x, y] = [0, 0, 255]  # Rouge
    
    
    
    '''# To draw the rectangle that correspond of the 2d field
    for key in dictionnaryCoords:
        x, y  = dictionnaryCoords[key]
        image[y, x+1100] = [0, 0, 255]  # Rouge'''

    # Show image of the detected field
    cv2.imshow('Field', image)
    # Afficher l'image (facultatif)
    

    cv2.waitKey(0)
    cv2.destroyAllWindows()"""
    
    return(dictionnaryCoords,treeCoords,allAnnotedCoords)
    

    

    
    





def getImageImpact(imageTerrain,dictionnaryCoords,treeCoords,allAnnotedCoords, coordImpact,colorImpact, rectangleWidth = global_rectangle_width,rectangleHeight=global_rectangle_height):
    tailleImpact = int(global_rectangle_width /50)
    # Get the nearest coord through the tree
    nearestCoord = coordonnee_plus_proche_kd(coordImpact, treeCoords,allAnnotedCoords)
    # Associate coord on the rectangle of the impact due to the nearest coord
    coordOnRectangle = dictionnaryCoords[nearestCoord]
    # Show the 2d field 
    imageTerrainRedimensionner = imageTerrain.resize((rectangleWidth, rectangleHeight))

    colorierPil(imageTerrainRedimensionner,coordOnRectangle[1], coordOnRectangle[0],colorImpact,tailleImpact)
    
    
    
    return(imageTerrainRedimensionner)
