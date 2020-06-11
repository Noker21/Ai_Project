from jeulib import Jeu
import joueurlib
import AI
import numpy as np

Ran = AI.Random
Hum = joueurlib.Humain
MM  = AI.MinMax

J = Jeu(opts={"choix_joueurs" : {"noir":MM, "blanc":MM}})
#J = Jeu()
J.demarrer()