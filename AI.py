from joueurlib import IA

from interfacelib import couleur_to_couleurval as Cl_val
import numpy as np

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

	def getValue(self):
		score = self.jeu.plateau.score()
		B_Score, W_Score = score[1], score[2]
		return B_Score - W_Score if self.couleur == "noir" else W_Score - B_Score

	def demande_coup(self):
		Possible_Moves = self.jeu.plateau.liste_coups_valides(Cl_val(self.couleur))
		if len(Possible_Moves) == 0 :
			return []

		BestScore = -float("inf")
		Chosen_Move = []

		for Move in Possible_Moves :
			Tmp_Board = self.jeu.plateau.copie()
			Tmp_Board.jouer(Move, Cl_val(self.couleur))
			Score = self.min_max(Tmp_Board, 3, False)
			if BestScore <= Score :
				BestScore = Score
				Chosen_Move = Move
		return Chosen_Move

	def min_max(self, Board, Depth, onMaximizing):		

		Possible_Moves = Board.liste_coups_valides(Cl_val(self.couleur))		
		if Depth == 0 or len(Possible_Moves) == 0:
			return self.getValue()

		BestScore = -float("inf") if onMaximizing else float("inf")

		if onMaximizing :
			for Move in Possible_Moves :
				Tmp_Board = Board.copie()
				Tmp_Board.jouer(Move, Cl_val(self.couleur))
				Score = self.min_max(Tmp_Board, Depth - 1, not onMaximizing)
				BestScore = max(Score, BestScore)
			return BestScore
		else :	
			for Move in Possible_Moves :
				Tmp_Board = Board.copie()
				Tmp_Board.jouer(Move, Cl_val(self.couleur))
				Score = self.min_max(Tmp_Board, Depth - 1, onMaximizing)
				BestScore = min(Score, BestScore)
			return BestScore
