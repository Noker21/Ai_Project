from jeulib import Jeu
import joueurlib
import AI
import numpy as np

Ran = AI.Random
Hum = joueurlib.Humain
MM  = AI.MinMax
AB  = AI.AlphaBeta

J = Jeu(opts={"choix_joueurs" : {"noir":MM, "blanc":MM}})
# J = Jeu()
J.demarrer()

# J2 = Jeu(opts={"choix_joueurs" : {"noir":AB, "blanc":AB}})
# J2.demarrer()