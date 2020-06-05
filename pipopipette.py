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
couleur_point = "#e863eb"
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

    if type == "ligne" and statut_ligne[x][y] == 0: #si dans le tableau des lignes la valeur est égale à zero, pas occupée
        occupee = False
    if type == "colonne" and statut_colonne[x][y] == 0:#idem mais pour les colonnes
        occupee = False

    return occupee

def update_jeu(type, position_jeu):
    y = position_jeu[0]
    x = position_jeu[1]
    valeur = 1
    if tour_joueur1:
        valeur =-1
    if x < (nombre_points - 1) and y < (nombre_points - 1):
        statut_jeu[x] #fonction pas encore recopiée, c'est la prochaine

def click(event): #fonction qui est appellée quand le joueur clique
    position_ecran = [event.x, event.y] #recupération de la position du click sur l'écran
    print("position ecran : ", position_ecran)
    position_jeu, type = convertir_position_ecran_vers_jeu(position_ecran) # convertit la position sur l'écran en position sur le jeu + le type de clic (ligne, colonne, ou invalide)
    print("position jeu : ", position_jeu, "type  : ", type)
    print("grille occupee : ", grille_occupee(position_jeu, type)) #regarde dans les tableaux si la ligne/colonne est occupée
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
statut_ligne = np.zeros(shape=(nombre_points - 1, nombre_points)) #le gars a inversé les tailles des tableau des lignes et des colonnes
statut_colonne = np.zeros(shape=(nombre_points, nombre_points - 1)) #je l'ai remis correctement mais il faut faire gaffe à ça en recopiant la suite
cases_cochees = []
#--------------------------------------
#Mainloop, je sais toujours pas ce que ça fait mais sinon le code se lance pas
#--------------------------------------
window.mainloop()
