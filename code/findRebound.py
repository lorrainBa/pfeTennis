import numpy as np

import cv2  # OpenCV is used for video processing
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

def detect_bounce(processedCoordonateData, decalageTerrainX, decalageTerrainY, large_window=80, small_window=10, polyorder=3, percentile=75, dy_threshold=0.5, base_frame_adjustment=0, y_weight=1.2, velocity_multiplier=10):
    x = processedCoordonateData[0]
    y = processedCoordonateData[1]
    t = processedCoordonateData[2]

    # Lisser les données de y avec les deux valeurs de window_length
    y_smooth_large = savgol_filter(y, window_length=large_window, polyorder=polyorder)
    y_smooth_small = savgol_filter(y, window_length=small_window, polyorder=polyorder)
    
    # Calculer les dérivées première pour les deux lissages
    dy_large = np.gradient(y_smooth_large)
    dy_small = np.gradient(y_smooth_small)

    # Détecter les grandes variations de y (frappes) pour les deux lissages
    large_variations_large = np.where(np.abs(dy_large) > np.percentile(np.abs(dy_large), percentile))[0]
    large_variations_small = np.where(np.abs(dy_small) > np.percentile(np.abs(dy_small), percentile))[0]

    # Fonction pour calculer le décalage en fonction de la vitesse
    def calculate_frame_adjustment(velocity):
        if velocity < 70:  # Balle lente
            return base_frame_adjustment
        elif velocity < 150:  # Balle moyenne
            return base_frame_adjustment + 1
        else:  # Balle rapide
            return base_frame_adjustment + 2

    # Identifier les rebonds entre chaque paire de grandes variations pour les deux lissages
    rebound_positions = {}
    for large_variations, dy in [(large_variations_large, dy_large), (large_variations_small, dy_small)]:
        for i in range(len(large_variations) - 1):
            start = large_variations[i]
            end = large_variations[i + 1]
            if end - start > 1:  # Assurer que le segment n'est pas vide
                segment_y = y[start:end]
                segment_t = t[start:end]

                # Calculer la vitesse moyenne de la balle dans le segment
                segment_x = x[start:end]
                if len(segment_t) > 1:  # Vérifier qu'il y a plus d'un point
                    weighted_distances = np.sqrt((np.diff(segment_x))**2 + (y_weight * np.diff(segment_y))**2)
                    velocities = (weighted_distances * velocity_multiplier) / np.diff(segment_t)
                    average_velocity = np.mean(velocities)
                else:
                    average_velocity = 0

                # Trouver le début de la stagnation au milieu du segment
                frame_adjustment = calculate_frame_adjustment(average_velocity)
                for j in range(start, end):
                    if np.abs(dy[j]) < dy_threshold:
                        adjusted_frame = max(start, j - frame_adjustment)  # Ajuster le point de détection vers l'arrière
                        rebound_positions[t[adjusted_frame]] = (int(x[adjusted_frame] - decalageTerrainX), int(y[adjusted_frame] - decalageTerrainY))
                        break  # Une fois le rebond trouvé, passer au segment suivant

    # Trier les positions de rebond par ordre chronologique
    sorted_rebound_positions = dict(sorted(rebound_positions.items()))

    return sorted_rebound_positions

def display_rebound_frames(video_path, rebound_positions, decalageX, decalageY):
    # Ouvrir la vidéo
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Erreur lors de l'ouverture de la vidéo.")
        return

    for frame_num, (x, y) in rebound_positions.items():
        x += decalageX
        y += decalageY
        # Définir la position de la vidéo à la frame désirée
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        
        ret, frame = cap.read()
        if not ret:
            print(f"Erreur lors de la lecture de la frame {frame_num}.")
            continue
        
        # Dessiner un point coloré sur les coordonnées de rebond
        cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)  # Dessiner un cercle vert
        
        # Afficher la frame
        plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        plt.title(f"Frame {frame_num} with rebound at ({x}, {y})")
        plt.show()

    cap.release()








def getTheBounceCoordinate(angleTrapez,processedCoordonateData):
    
    angleTrapez,decalageX,decalageY = decaler_points(angleTrapez)
    # ------------- TROUVER LES COORDOONNES ET LES FRAMES DE REBOND -------------
    rebound_positions_and_frame = detect_bounce(processedCoordonateData,decalageX,decalageY)
    return(rebound_positions_and_frame,decalageX,decalageY)





def decaler_points(trapeze):
    # Extraire les points du dictionnaire
    top_left = trapeze["top_left"]
    bottom_left = trapeze["bottom_left"]
    top_right = trapeze["top_right"]
    bottom_right = trapeze["bottom_right"]
    decalageGauche = int(bottom_left[0])
    top_left[0] -= decalageGauche
    bottom_left[0] -= decalageGauche
    top_right[0] -= decalageGauche
    bottom_right[0] -= decalageGauche
    #DEcalage bas
    if top_left[1] > top_right[1]:
        decalageHauteur = int(top_right[1])
    else:
        decalageHauteur = int(top_left[1])
    top_left[1] -= decalageHauteur
    bottom_left[1] -= decalageHauteur
    top_right[1] -= decalageHauteur
    bottom_right[1] -= decalageHauteur

    # Mettre à jour le dictionnaire
    trapeze["top_left"] = top_left
    trapeze["bottom_left"] = bottom_left
    trapeze["top_right"] = top_right
    trapeze["bottom_right"] = bottom_right

    return trapeze,decalageGauche,decalageHauteur

