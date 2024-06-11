import cv2







# Fonction pour trier les points en fonction de critères spécifiques
def getCoordsAngleTrapez(imgPath):
    # Charger votre image
    image = cv2.imread(imgPath, cv2.IMREAD_UNCHANGED)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Seuillage pour détecter les contours
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    # Recherche des contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Initialiser les coins supérieurs avec des valeurs extrêmes
    top_left = [float('inf'), float('inf')]
    top_right = [float('-inf'), float('inf')]
    
    # Parcourir tous les points des contours pour trouver les coins
    for contour in contours:
        for point in contour:
            point = point[0]  # Extraire le point du tableau numpy
            # Mettre à jour les coins supérieurs
            if (point[1] < top_left[1]+3) and (point[0] < top_left[0]):
                top_left = point
            if ( point[1] < top_right[1]+3) and (point[0] > top_right[0]):
                top_right = point
                
    # Initialiser les coins inférieurs avec les coordonnées des coins supérieurs
    bottom_left = [float('inf'), float('-inf')]
    bottom_right = [float('-inf'), float('-inf')]
    
    # Parcourir tous les points des contours pour trouver les coins inférieurs
    for contour in contours:
        for point in contour:
            point = point[0]  # Extraire le point du tableau numpy
            # Mettre à jour les coins inférieurs
            if point[0] < bottom_left[0] or (point[0] == bottom_left[0] and point[1] > bottom_left[1]):
                bottom_left = point
            if point[0] > bottom_right[0] or (point[0] == bottom_right[0] and point[1] > bottom_right[1]):
                bottom_right = point
                
    



    
    #Décaler les points pour les commencer en 0,0
    #DEcalage gauche
    decalageGauche = bottom_left[0]
    top_left[0] -= decalageGauche
    bottom_left[0] -= decalageGauche
    top_right[0] -= decalageGauche
    bottom_right[0] -= decalageGauche
    #DEcalage bas
    if top_left[1] > top_right[1]:
        decalageHauteur = top_right[1]
    else:
        decalageHauteur = top_left[1]
    top_left[1] -= decalageHauteur
    bottom_left[1] -= decalageHauteur
    top_right[1] -= decalageHauteur
    bottom_right[1] -= decalageHauteur
    # Associer les noms aux points
    points = {
        'top_left': top_left,
        'bottom_left': bottom_left,
        'top_right': top_right,
        'bottom_right': bottom_right
    }

    # Dessiner des cercles sur les points extrêmes pour vérification


    #To show the image
    for name, point in points.items():
        cv2.circle(image, (int(point[0]), int(point[1])), 5, (0, 0, 255), -1)
        cv2.putText(image, name, (point[0] - 20, point[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Affichage de l'image avec les points extrêmes
    cv2.imshow('Extreme Points', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return [top_left, bottom_left, top_right, bottom_right]


