import numpy as np

class Plateau:
	
	def __init__(self, taille=8):
		self.tableau_cases = [[0 for j in range(taille)] for i in range(taille)]
		self.tableau_cases[taille//2-1][taille//2-1] = -1 #initialisation des 4 premiers pions
		self.tableau_cases[taille//2][taille//2-1] = 1
		self.tableau_cases[taille//2-1][taille//2] = 1
		self.tableau_cases[taille//2][taille//2] = -1
		self.taille = taille		
		
	def jouer(self, case, couleurval):
		if case == []: #[] signifie que le joueur passe
			return not self.existe_coup_valide(couleurval)
		if self.est_coup_valide(case, couleurval):
			self.tableau_cases[case[0]][case[1]] = couleurval #on joue sur la case
			directions = [[int(round(np.cos(k*np.pi/4))), int(round(np.sin(k*np.pi/4)))] for k in range(8)] #liste des 8 directions
			for d in directions:
				if self.capture_ligne(case, couleurval, d):
					new_case = [case[0] + d[0], case[1] + d[1]]
					while self.tableau_cases[new_case[0]][new_case[1]] == -couleurval:
						self.tableau_cases[new_case[0]][new_case[1]] = couleurval
						new_case = [new_case[0] + d[0], new_case[1] + d[1]]
			return True
		return False

	def est_coup_valide(self, case, couleurval):
		if self.tableau_cases[case[0]][case[1]] != 0:
			return False #la case n'est pas vide

		flag_capture = False
		directions = [[int(round(np.cos(k*np.pi/4))), int(round(np.sin(k*np.pi/4)))] for k in range(8)] #liste des 8 directions
		for d in directions:
			if self.capture_ligne(case, couleurval, d):
				return True
		
		return False #le coup ne capture pas

	def existe_coup_valide(self, couleurval):
		for i in range(self.taille):
			for j in range(self.taille):
				if self.est_coup_valide([i,j], couleurval):
					return True
		return False

	def liste_coups_valides(self, couleurval):
		coups_valides = []
		for i in range(self.taille):
			for j in range(self.taille):
				if self.est_coup_valide([i,j], couleurval):
					coups_valides.append([i,j])
		return coups_valides

	def capture_ligne(self, case, couleurval, direction):
		'''capture_ligne(c, j, d) : retourne vrai lorsque le joueur avec la couleur j joue sur la case c et qu'une ligne adverse dans la direction d peut être capturée, faux sinon.'''
		new_case = [case[0] + direction[0], case[1] + direction[1]]
		entre_loop = False
		while (min(new_case[0], new_case[1]) >= 0 and max(new_case[0], new_case[1]) < self.taille
			 and self.tableau_cases[new_case[0]][new_case[1]] == -couleurval):
			new_case[0] += direction[0]
			new_case[1] += direction[1]
			entre_loop = True

		if min(new_case[0], new_case[1]) < 0 or max(new_case[0], new_case[1]) >= self.taille:
			return False
		if self.tableau_cases[new_case[0]][new_case[1]] != couleurval:
			return False
		return entre_loop
			

	def copie(self):
		copie = Plateau(self.taille)
		copie.tableau_cases = [[self.tableau_cases[i][j] for j in range(self.taille)] for i in range(self.taille)]
		return copie

	def score(self):
		noir = 0
		blanc = 0
		for i in range(self.taille):
			for j in range(self.taille):
				if self.tableau_cases[i][j] == 1:
					noir += 1
				if self.tableau_cases[i][j] == -1:
					blanc += 1
		victoire_noir = 1 if noir > blanc else -1 if blanc > noir else 0
		return [victoire_noir, noir, blanc]