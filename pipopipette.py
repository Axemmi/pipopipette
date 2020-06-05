from tkinter import *
import numpy as np

#--------------------------------------
#Variables
#--------------------------------------
dimensions_fenetre = 600 #largeur et hauteur de la fenêtre, en pixels
nombre_points = 4 #nombre de points constituant la largeur du jeu, ex : 4 points équivaut 3x3 cases
epaisseur_point = 0.25 * dimensions_fenetre / nombre_points #l'épaisseur d'un point, en fonction de la taille de la fenêtre
epaisseur_trait = 0.1 * dimensions_fenetre / nombre_points #idem mais pour les traits
distance_entre_points = dimensions_fenetre / nombre_points #distance entre les points
couleur_point = "#2e2e2e"
couleur_joueur1 = "#53bfe6"
couleur_joueur2 = "#e83162"
couleur_joueur1_carre = "#b8d9e6"
couleur_joueur2_carre = "#e8bac6"
tour_joueur1 = True #si true = au tour du joueur 1, si false au tour du joueur 2
fin_du_jeu = False 
#--------------------------------------
#Fonctions
#--------------------------------------
def afficher_grille(): #bah ça affiche la grille vierge, donc les traits en pointillés et les ronds, les traits rouge ou bleu sont gérés ailleurs
    for i in range(nombre_points):
        x = i*distance_entre_points+distance_entre_points/2
        canvas.create_line(x, distance_entre_points/2, x, dimensions_fenetre-distance_entre_points/2, fill='gray', dash = (2, 2))
        canvas.create_line(distance_entre_points/2, x, dimensions_fenetre-distance_entre_points/2, x, fill='gray', dash=(2, 2))

    for i in range(nombre_points):
        for j in range(nombre_points):
            start_x = i*distance_entre_points+distance_entre_points/2
            end_x = j*distance_entre_points+distance_entre_points/2
            canvas.create_oval(start_x-epaisseur_point/2, end_x-epaisseur_point/2, start_x+epaisseur_point/2, end_x+epaisseur_point/2, fill=couleur_point, outline=couleur_point)

def convertir_position_ecran_vers_jeu(position_ecran):
    position_ecran = np.array(position_ecran) #en gros ça convertit la position du click qui est un array basique [x,y] en array de type numpy, surement que numpy a des fonctions qui seront utiles plus tard
    position = (position_ecran - distance_entre_points/4)//(distance_entre_points/2) #je sais pas comment ça marche, mais position en pixels --> position sur le plateau
    print("position sur le plateau : ", position)

    type = False
    position_jeu = []
    if position[1] % 2 == 0 and (position[0] - 1) % 2 == 0 : #si la position verticale sur le plateau est paire et que la position en x est impaire, donc que c'est trait horizontal sur la même ligne qu'un point (pas le millieu d'un carré quoi)
        x = int((position[0]-1)//2)
        y = int(position[1]//2)
        position_jeu = [x, y]
        type = 'ligne'

    elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0: #pareil mais pour un trait vertical du coup
        x = int(position[0] // 2)
        y = int((position[1] - 1) // 2)
        position_jeu = [x, y]
        type = 'colonne'

    return position_jeu, type

def grille_occupee(position_jeu, type): #regarde dans les tableau si les lignes colonnes sont occupées, à savoir si la valeur est -1 pour le joueur 1 et 1 pour le joueur 2
    x = position_jeu[0]
    y = position_jeu[1]
    occupee = True

    if type == "ligne" and statut_ligne[y][x] == 0: #si dans le tableau des lignes la valeur est égale à zero, pas occupée
        occupee = False
    if type == "colonne" and statut_colonne[y][x] == 0:#idem mais pour les colonnes
        occupee = False

    return occupee

def update_jeu(position_jeu, type): #mise à jour des tableaux, pour l'instant que les lignes et les colonnes, pas les carrés
    x = position_jeu[0]
    y = position_jeu[1]

    valeur = 1 #la valeur à ajouter / enlever selon le joueur ; rappel : si un carré arrive à 4 ou -4, il est remporté
    if tour_joueur1:
        valeur =-1

    if x < (nombre_points-1) and y < (nombre_points-1): #mise à jour du tableau des carrés
        statut_jeu[y][x] += valeur

    if type == 'ligne': # mise à jour du tableau des lignes
        statut_ligne[y][x] = 1
        if y >= 1 : # cas supplémentaire pour le tableau des carrés
            statut_jeu[y-1][x] += valeur

    elif type == 'colonne': #idem pour les colonnes
        statut_colonne[y][x] = 1
        if x >= 1 : # idem, cas supplémentaire pour le tableau des carrés
            statut_jeu[y][x-1] += valeur

def tracer_trait(position_jeu, type):
    if type == 'ligne':
        debut_x = distance_entre_points / 2 + position_jeu[0] * distance_entre_points
        fin_x = debut_x + distance_entre_points
        debut_y = distance_entre_points / 2 + position_jeu[1] * distance_entre_points
        fin_y = debut_y
    elif type == 'colonne':
        debut_y = distance_entre_points / 2 + position_jeu[1] * distance_entre_points
        fin_y = debut_y + distance_entre_points
        debut_x = distance_entre_points / 2 + position_jeu[0] * distance_entre_points
        fin_x = debut_x

    if tour_joueur1:
        couleur = couleur_joueur1
    else:
        couleur = couleur_joueur2

    canvas.create_line(debut_x, debut_y, fin_x, fin_y, fill = couleur, width = epaisseur_trait)

def trouver_carre():
    carres = np.argwhere(statut_jeu == -4) #on récupère tout les carrés pour lesquels la valeur est -4, donc ceux remportés par le joueur 1
    couleur = couleur_joueur1_carre
    for carre in carres:
        dessiner_carre(carre, couleur)

    carres = np.argwhere(statut_jeu == 4) #idem mais ceux pour lesquels la valeur est 4, donc remportés par le joueur 2
    couleur = couleur_joueur2_carre
    for carre in carres:
        dessiner_carre(carre, couleur)

def dessiner_carre(carre, couleur):
    debut_x = distance_entre_points / 2 + carre[1] * distance_entre_points + epaisseur_trait/2
    debut_y = distance_entre_points / 2 + carre[0] * distance_entre_points + epaisseur_trait/2
    fin_x = debut_x + distance_entre_points - epaisseur_trait
    fin_y = debut_y + distance_entre_points - epaisseur_trait
    canvas.create_rectangle(debut_x, debut_y, fin_x, fin_y, fill = couleur, outline = "")

def verifier_fin_du_jeu :

#--------------------------------------
#Fonction appelée quand on clique, où est gérée la plupart de la logique du déroulement du jeu
#--------------------------------------
def click(event):

    verifier_fin_du_jeu()

    position_ecran = [event.x, event.y] #recupération de la position du click sur l'écran
    print("position ecran : ", position_ecran)

    position_jeu, type = convertir_position_ecran_vers_jeu(position_ecran) # convertit la position sur l'écran en position sur le jeu + le type de clic (ligne, colonne, ou invalide)
    print("position jeu : ", position_jeu, "type  : ", type)

    if type and not grille_occupee(position_jeu, type): #si la position cliqué est une ligne / colonne non occupée
        update_jeu(position_jeu, type) #mettre à jour les tableaux
        print("statut ligne : ", "\n", statut_ligne)
        print("statut colonne : ","\n", statut_colonne)
        print("statut jeu : ", "\n", statut_jeu)

        tracer_trait(position_jeu, type) #trace le trait bleu ou rouge
        trouver_carre() #trouve les carrés qui ont étés complétés, et appelle une fonction pour les tracer
        afficher_grille() # on redessine la grille par dessus

        global tour_joueur1 #ensuite on inverse la bool globale tour_joueur1
        tour_joueur1 = not tour_joueur1 #ça a son importance pour la valeur a ajouter au carré ou la couleur des traits par exemple
        print("Tour Joueur 1 : ", tour_joueur1)
#--------------------------------------
#Création de la fenêtre + affichage
#--------------------------------------
window = Tk()
window.title('Pipopipette')
canvas = Canvas(window, width=dimensions_fenetre, height=dimensions_fenetre)
canvas.pack()
window.bind('<Button-1>', click) #on lie le bouton gauche de la souris avec la fonction click (au dessus)
tour_joueur1 = True
afficher_grille()
#--------------------------------------
#Initialisation des tableaux
#--------------------------------------
statut_jeu = np.zeros(shape=(nombre_points - 1, nombre_points - 1)) #tableau des carrés
statut_ligne = np.zeros(shape=(nombre_points, nombre_points - 1)) #la fonction numpy.zeros crée un tableau de la forme (taille y; taille x) donc c'est inversé
statut_colonne = np.zeros(shape=(nombre_points - 1, nombre_points)) #donc à chaque fois qu'on recupère une valeur dans un array numpy c'est [y][x]
cases_cochees = []
#--------------------------------------
#Mainloop, je sais toujours pas ce que ça fait mais sinon le code se lance pas
#--------------------------------------
window.mainloop()
