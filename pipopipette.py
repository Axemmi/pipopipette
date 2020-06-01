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
def afficher_grille(): #bah ça affiche la grille vierge, donc les traits en pointillés et les ronds, les traits rouge ou bleu sont gérés ailleurss
    for i in range(nombre_points):
        x = i*distance_entre_points+distance_entre_points/2
        canvas.create_line(x, distance_entre_points/2, x, dimensions_fenetre-distance_entre_points/2, fill='gray', dash = (2, 2))
        canvas.create_line(distance_entre_points/2, x, dimensions_fenetre-distance_entre_points/2, x, fill='gray', dash=(2, 2))

    for i in range(nombre_points):
        for j in range(nombre_points):
            start_x = i*distance_entre_points+distance_entre_points/2
            end_x = j*distance_entre_points+distance_entre_points/2
            canvas.create_oval(start_x-epaisseur_point/2, end_x-epaisseur_point/2, start_x+epaisseur_point/2, end_x+epaisseur_point/2, fill=couleur_point, outline=couleur_point)
#--------------------------------------
#Création de la fenêtre + affichage
#--------------------------------------
window = Tk()
window.title('Pipopipette')
canvas = Canvas(window, width=dimensions_fenetre, height=dimensions_fenetre)
canvas.pack()
# window.bind('<Button-1>', click) --> fonction click pas encore crée, je commente pour éviter les erreurs
tour_joueur1 = True
afficher_grille()

#--------------------------------------
#Mainloop, je sais toujours pas ce que ça fait mais sinon le code se lance pas
#--------------------------------------
window.mainloop()
