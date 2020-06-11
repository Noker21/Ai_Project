#!/usr/bin/python
# coding: utf8

from __future__ import division
from Board import Plateau

import joueurlib
import AI
import interfacelib



class Jeu:
	
	def __init__(self, taille=8, opts={}):
		if "choix_joueurs" not in opts :
			possibilites = [joueurlib.Humain] + joueurlib.IA.__subclasses__()
			if len(possibilites) == 1:
				print("Un seul type de joueur est actuellement implémenté : "+
					  str(possibilites[0])+".\nCe type sera choisi pour noir et blanc.")
				self.noir = possibilites[0](self, "noir", opts)
				self.blanc = possibilites[0](self, "blanc", opts)
			else:
				print("Quel type de joueur souhaitez vous sélectionner pour noir ?",
					  "Les possibilités sont :")
				for i in range(len(possibilites)):
					print(i+1," : "+str(possibilites[i]))
				choix = input("Tapez le nombre correspondant.\n")
				self.noir = possibilites[int(choix)-1](self, "noir", opts)
				print("Quel type de joueur souhaitez vous sélectionner pour blanc ?\nLes possibilités sont :")
				for i in range(len(possibilites)):
					print(i+1," : "+str(possibilites[i]))
				choix = input("Tapez le nombre correspondant.\n")
				self.blanc = possibilites[int(choix)-1](self, "blanc", opts)
		else : 
			self.noir  = opts["choix_joueurs"]["noir"](self, "noir")
			self.blanc = opts["choix_joueurs"]["blanc"](self, "blanc")

		self.plateau = Plateau(taille)
		self.tour = 1
		self.precedent_passe = False
		self.partie_finie = False
		self.joueur_courant = self.noir
		
		if "interface"  not in opts or opts["interface"]:
			self.interface = True
			self.gui = interfacelib.Interface(self)
		else:
			self.interface = False

	def demarrer(self):
		if isinstance(self.joueur_courant, joueurlib.IA):
			self.gui.active_ia()
		else:
			self.gui.active_humain()
		self.gui.fenetre.mainloop()
		
	def jouer(self, coup):
		self.plateau.jouer(coup, interfacelib.couleur_to_couleurval(self.joueur_courant.couleur))
		if self.interface:
			self.gui.actualise_plateau()
		
		self.tour += 1
		if coup == []:
			if self.precedent_passe:
				self.partie_finie = True
			self.precedent_passe = True
		else:
			self.precedent_passe = False
		
		if self.partie_finie:
			[v, s_noir, s_blanc] = self.score()
			if v == 0:
				m = "la partie est un nul, avec "+str(s_noir)+" points chacun."
			elif v == 1:
				m = "Victoire de noir, avec "+str(s_noir)+" points contre "+str(s_blanc)+'.'
			elif v == -1:
				m = "Victoire de blanc, avec "+str(s_blanc)+" points contre "+str(s_noir)+'.'
			print(m)
			if self.interface:
				self.gui.desactive_humain()
				self.gui.desactive_ia()
				self.gui.message_tour.set("Partie finie.\n"+m)
			self.joueur_courant = None
				
		else:
			if self.tour%2 == 1:
				self.joueur_courant = self.noir
				if self.interface:
					self.gui.message_tour.set("A noir de jouer")
			else:
				self.joueur_courant = self.blanc
				if self.interface:
					self.gui.message_tour.set("A blanc de jouer")

	def score(self):
		return self.plateau.score()

			
			
