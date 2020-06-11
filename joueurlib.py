class Joueur:
	def __init__(self, partie, couleur, opts={}):
		self.couleur = couleur
		self.jeu = partie
		self.opts = opts

	def demande_coup(self):
		pass


class Humain(Joueur):

	def demande_coup(self):
		pass



class IA(Joueur):

	def __init__(self, partie, couleur, opts={}):
		super().__init__(partie,couleur,opts)
		self.temps_exe = 0
		self.nb_appels_jouer = 0
	def demande_coup(self):
		pass
