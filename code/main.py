
from associateCoordToRectangle import processFieldAndCoordonate, getImageImpact
from findRebound import getTheBounceCoordinate, display_rebound_frames
from makeVideoOfCourt import generateVideoOfCourt
from PIL import Image
import pickle
import numpy as np





# FONCTIONNEMENT PROGRAMME
def main():
    # ------------- EN ENTRER OUVRIR IMAGE DESSIN TERRAIN DE TENNIS ET VOS COORDONNES -------------
    video_path = "data/video/video15_output_v4.avi"
    gameBallCoordinatePath = "data/coordonateData/ball_track15_v4.pkl"
    angleTrapez = {
        "top_left": [419  ,161],
        "top_right": [877 ,161],
        "bottom_left": [201 ,652],
        "bottom_right": [1095 ,655]
    }


    processedCoordonateData = processData(gameBallCoordinatePath)
    rebound_positions_and_frame,decalageX,decalageY = getTheBounceCoordinate(angleTrapez,processedCoordonateData)
    print(rebound_positions_and_frame)
    # ------------- PUIS FAIRE LE TERRAIN ARTIFICIEL UNE FOIS -------------
    dictionnaryCoords,treeCoords,allAnnotedCoords = processFieldAndCoordonate(angleTrapez)
    

    

    # PUIS PRENDRE COORD D'UN IMPACT ET ITERER AUTANT DE FOIS QUE VOUS VOULEZS SUR getImageImpact
    # CETTE FONCTION RENVOIE LA PHOTO MODIFIER DONC IL FAUDRA ITERER SUR CETTE PHOTO MODIFIER
    # Coord d'un impact
    # Afficher l'image pour tester
    
    #display_rebound_frames(video_path, rebound_positions_and_frame, decalageX,decalageY)

    imageWithRebond = Image.open("data/terrain.png")
    for rebound in rebound_positions_and_frame:
        currentCoordImpact = rebound_positions_and_frame[rebound]
        imageWithRebond = getImageImpact(imageWithRebond,dictionnaryCoords,treeCoords,allAnnotedCoords, currentCoordImpact,(255,0,0))
    #imageWithRebond.show()
    
    generateVideoOfCourt(video_path,   dictionnaryCoords,treeCoords,allAnnotedCoords,   processedCoordonateData,   rebound_positions_and_frame, decalageX,decalageY)

    




def processData(file_path):
    # Charger les données depuis le fichier pickle
    with open(file_path, "rb") as f:
        data = pickle.load(f)

    # Initialiser les listes pour les cadres et les coordonnées
    frames = []
    x_coords = []
    y_coords = []

    # Filtrer les valeurs None et les ajouter aux listes
    for i, val in enumerate(data):
        if val[0] is not None and val[1] is not None:
            frames.append(i)
            x_coords.append(int(val[0]))  # Conversion en entier
            y_coords.append(int(val[1]))  # Conversion en entier

    # Convertir les listes en tableaux numpy
    x = np.array(x_coords)
    y = np.array(y_coords)
    t = np.array(frames)
    return(x,y,t)





main()

