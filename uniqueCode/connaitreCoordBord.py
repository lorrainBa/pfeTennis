import cv2
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseEvent

def on_mouse_move(event: MouseEvent):
    if event.inaxes:
        x, y = int(event.xdata), int(event.ydata)
        print(f"Coordonnées du pixel : x={x}, y={y}")

def show_first_frame(video_path: str):
    # Ouvrir la vidéo
    cap = cv2.VideoCapture(video_path)
    
    # Vérifier si la vidéo est ouverte correctement
    if not cap.isOpened():
        print("Erreur: Impossible d'ouvrir la vidéo.")
        return

    # Lire la première frame
    ret, frame = cap.read()

    # Libérer la vidéo
    cap.release()

    if not ret:
        print("Erreur: Impossible de lire la première image de la vidéo.")
        return

    # Convertir l'image de BGR (format OpenCV) à RGB (format Matplotlib)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Afficher l'image avec Matplotlib
    fig, ax = plt.subplots()
    ax.imshow(frame)
    plt.show()

# Exemple d'utilisation
video_path = "data/video/video12_output_v4.avi"
show_first_frame(video_path)
