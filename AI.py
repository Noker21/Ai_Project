from joueurlib import IA

from interfacelib import couleur_to_couleurval as Cl_val
import numpy as np
from time import time as getTime

class Random(IA):
	def demande_coup(self):
		Possible_Moves = self.jeu.plateau.liste_coups_valides(Cl_val(self.couleur))
		lenght = len(Possible_Moves)
		if lenght == 0:
			return []
		rand = np.random.randint(lenght)
		coup = [Possible_Moves[rand][0],Possible_Moves[rand][1]]
		return coup

class MinMax(IA):

	Nbr_Simulated_Moves = 0

	def demande_coup(self):
		Start = getTime() 
		self.Nbr_Simulated_Moves = 0
		Possible_Moves = self.jeu.plateau.liste_coups_valides(Cl_val(self.couleur))
		
		if len(Possible_Moves) == 0 :
			return []

		BestScore = -float("inf")
		Chosen_Move = []
		print(self.couleur, " : ")
		for Move in Possible_Moves :
			Tmp_Board = self.jeu.plateau.copie()
			Tmp_Board.jouer(Move, Cl_val(self.couleur))
			self.Nbr_Simulated_Moves += 1
			Score = self.min_max(Tmp_Board, 3, False, Cl_val(self.couleur))
			print("\t", Move, " ==> ", Score)
			if BestScore <= Score :
				BestScore = Score
				Chosen_Move = Move
		End = getTime()
		print("\n\tChosen Move ==> ", Chosen_Move, " after ", self.Nbr_Simulated_Moves, " simulations (",End-Start," s )")
		return Chosen_Move
	
	def min_max(self, Board, Depth, onMaximizing, Color):		
		if Depth == 0 :
			return getValue(Board, Color)

		BestScore = -float("inf") if onMaximizing else float("inf")

		if onMaximizing :
			Possible_Moves = Board.liste_coups_valides(Color)
			for Move in Possible_Moves :
				Tmp_Board = Board.copie()
				Tmp_Board.jouer(Move, Color)
				self.Nbr_Simulated_Moves += 1
				Score = self.min_max(Tmp_Board, Depth - 1, not onMaximizing, -Color)
				BestScore = max(Score, BestScore)
			return BestScore

		else :	
			Possible_Moves = Board.liste_coups_valides(-Color)
			for Move in Possible_Moves :
				Tmp_Board = Board.copie()
				Tmp_Board.jouer(Move, -Color)
				self.Nbr_Simulated_Moves += 1
				Score = self.min_max(Tmp_Board, Depth - 1, not onMaximizing, -Color)
				BestScore = min(Score, BestScore)
			return BestScore

class AlphaBeta(IA):
	
	def demande_coup(self):
		Start = getTime() 
		self.Nbr_Simulated_Moves = 0
		Possible_Moves = self.jeu.plateau.liste_coups_valides(Cl_val(self.couleur))
		
		if len(Possible_Moves) == 0 :
			return []

		BestScore = -float("inf")
		Chosen_Move = []
		print(self.couleur, " : ")
		for Move in Possible_Moves :
			Tmp_Board = self.jeu.plateau.copie()
			Tmp_Board.jouer(Move, Cl_val(self.couleur))
			self.Nbr_Simulated_Moves += 1
			Score = self.alpha_beta(Tmp_Board, 3, False, Cl_val(self.couleur))
			print("\t", Move, " ==> ", Score)
			if BestScore <= Score :
				BestScore = Score
				Chosen_Move = Move
		End = getTime()
		print("\n\tChosen Move ==> ", Chosen_Move, " after ", self.Nbr_Simulated_Moves, " simulations (",End-Start," s )")
		return Chosen_Move

	def alpha_beta(self, Board, Depth, onMaximizing, Color, Alpha=-float("inf"), Beta=float("inf")):		
	
		if Depth == 0 :
			return getValue(Board, Color)

		BestScore = -float("inf") if onMaximizing else float("inf")

		if onMaximizing :
			Possible_Moves = Board.liste_coups_valides(Color)
			for Move in Possible_Moves :
				Tmp_Board = Board.copie()
				Tmp_Board.jouer(Move, Color)
				self.Nbr_Simulated_Moves += 1
				Score = self.alpha_beta(Tmp_Board, Depth - 1, not onMaximizing, -Color)
				BestScore = max(Score, BestScore)
				Alpha = max(Alpha,BestScore)
				if Alpha >= Beta :
					break
			return BestScore

		else :	
			Possible_Moves = Board.liste_coups_valides(-Color)
			for Move in Possible_Moves :
				Tmp_Board = Board.copie()
				Tmp_Board.jouer(Move, -Color)
				self.Nbr_Simulated_Moves += 1
				Score = self.alpha_beta(Tmp_Board, Depth - 1, not onMaximizing, -Color)
				BestScore = min(Score, BestScore)
				Beta = min(Beta, BestScore)
				if Beta <= Alpha :
					break
			return BestScore		

def getValue(Board, Color):
	My_Score, Enm_Score = 0, 0
	for i in range(8):
		for j in range(8):
			if Board.tableau_cases[i][j] == Color:
				if i in [0,7] and j in [0, 7]:
					if i == j or [i, j] == [0, 7] or [i, j] == [7, 0]: 
						My_Score += 5
					My_Score += 5
				My_Score += 1
			elif Board.tableau_cases[i][j] == -Color:
				if i in [0,7] and j in [0, 7]:
					if i == j or [i, j] == [0, 7] or [i, j] == [7, 0]: 
						Enm_Score += 5
					Enm_Score += 5
				Enm_Score += 1
	return My_Score - Enm_Score
