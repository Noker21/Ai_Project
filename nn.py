#!/usr/bin/env python

import numpy as np
import sys
import scipy.optimize
import matplotlib.pyplot as plt




def sigmoid_lecun(z, grad=False):
	'''Takes a real value z and returns 1.7159 tanh(2z/3). If z = (z_i) is a vector, returns (sigmoid(z_i)). This is the
	 recommended activation function. If grad is True, returns gradient of the function at z instead.'''
	if grad:
		return 1.7159 * tanh(z, grad)
	else:
		return 1.7159 * tanh(z, grad)

		
def sigmoid(z, grad=False):
	'''Takes a real value z and returns 1.7159 tanh(2z/3). If z = (z_i) is a vector, returns (sigmoid(z_i)). This is the
	 recommended activation function. If grad is True, returns gradient of the function at z instead.'''
	if grad:
		return 1.7159 * tanh(z, 2 / 3, True)
	else:
		return 1.7159 * tanh(z, 2 / 3)


def tanh(z, alpha=1, grad=False):
	'''Takes a real value z and returns tanh(x) = (1 - np.exp(- 2 * alpha * z)) / (1 + np.exp(- 2 * alpha * z)),
	the hyperbolic tangent of z lying in (-1,1), parametrized by alpha (with default value 1). If z = (z_i) is a vector,
	 returns (tanh(z_i)). If grad is True, returns gradient of the function at z instead.'''
	if grad:
		return alpha * (1 - tanh(z, alpha)**2)
	else:
		return (1 - np.exp(- 2 * alpha * z)) / (1 + np.exp(- 2 * alpha * z))


def pos(x):
	if x > 0:
		return 1
	else:
		return 0


def relu(z, grad=False):
	if not grad:
		return np.maximum(0, z)
	else:
		return pos(z)


def logistic(z, alpha=1):
	'''Takes a real value z and returns 1 / (1 + np.exp(- 2 * alpha * z)) which lies in (0,1), parametrized by alpha
	(with default value 1). If z = (z_i) is a vector, returns (tanh(z_i)). If grad is True, returns gradient of the function at z instead.'''
	if grad:
		y = logistic(z, alpha)
		return alpha * y * (1 - y)
	return 1 / (1 + np.exp(- alpha * z))


def delta(i,j):
	if i == j:
		return 1
	return 0


def softmax(z, jac=False):
	'''softmax(z, jac). Takes a vector z and returns (exp(z_i) / 
	sum_{j=1}^{len(z)} exp(z_j). If jac is True (False by default), 
	returns the Jacobian of the softmax function instead.'''
	M = max(z)
	if not jac:
		return np.exp(z-M) / np.sum(np.exp(z-M))
	else:
		res = softmax(z)
		
		return np.array([[res[i] * (delta(i,j) - res[j]) for j in range(len(res))] for i in range(len(res))]) #peut etre qu'il faut transposer



class PerceptronMulticouche:

	def __init__(self, taille_entree, couches=[], opts={}):

		self.sorties = []
		self.taille_entree = taille_entree

		self.nb_params = 0
		self.layers = []
		if len(couches) > 0:
			self.ajout_layer(taille_entree, couches[0])
			#self.layers = [Layer(taille_entree, couches[0])]
			for i in range(1, len(couches)):
				if i==len(couches)-1 and ("classification" not in opts or opts["classification"]):
					self.ajout_layer(self.layers[-1], couches[i], softmax)
					self.erreur = lambda xs, ys: entropie_croisee(xs, ys, self)
				else:
					self.ajout_layer(self.layers[-1], couches[i])
		
	def ajout_layer(self, entree, taille_sortie, activation=relu):
		print("ajout d'une couche avec entree "+str(entree)+" et sortie "+str(taille_sortie))
		new_layer = Layer(entree, taille_sortie, activation)
		self.layers.append(new_layer)
		if isinstance(entree, Layer):
			self.sorties.remove(entree)
			self.nb_params += (entree.shape[1]+1) * taille_sortie
		elif isinstance(entree, int):
			self.nb_params += (entree+1) * taille_sortie
		else:
			raise ValueError("Mauvais type d'entree. Entree recue : "+str(entree))
		self.sorties.append(new_layer)

	def __call__(self, x):
		if len(self.sorties) == 1:
			return self.sorties[0](x)
		else:
			return [s(x) for s in self.sorties]

	def get_params(self):
		return np.concatenate([l.get_params() for l in self.layers])

	def set_params(self, p):
		cpt = 0
		for l in self.layers:
			l.set_params(p[cpt:cpt+l.nb_params])
			cpt += l.nb_params

	def grad(self, x):
		'''pas encore implemente'''
		pass
		#if len(self.sorties) > 1:
		#	raise ValueError("pas encore implemente pour plusieurs sorties")
		#grad_erreur = self.erreur
		
def precision(xs, ys, classificateur):
	'''precision(xs, ys, classificateur) rend la proportion de points de xs pour lesquels le classificateur prédit correctement la classe ys.'''
	assert classificateur.taille_entree == len(xs[0])
	assert len(xs) == len(ys)
	nb_bons = 0
	for i in range(len(xs)):
		pred = classificateur(xs[i])
		if np.argmax(ys[i]) == np.argmax(pred):
			nb_bons += 1
	return nb_bons / len(xs)
			
def entropie_croisee(xs, ys, classificateur, grad=False):
	'''entropie_croisee(xs, ys, classificateur) : rend l'entropie croisée 
	de la prédiction des points contenus dans la liste xs par le 
	classificateur, contre les valeurs cibles de ys. Les valeurs de ys 
	doivent être un vecteur de 1 ou 0, pas de valeurs entre ces deux nombres.'''
	assert classificateur.taille_entree == len(xs[0])
	assert len(xs) == len(ys)
	preds = [classificateur(x) for x in xs]
	assert len(preds[0]) == len(ys[0])
	if not grad:
		erreur = 0
		for i in range(len(ys)):
			for j in range(len(ys[i])):
				if ys[i][j] == 1:
					erreur -= np.log(preds[i][j])
		return erreur / len(ys)
	else:
		grad = 0
		for i in range(len(ys)):
			for j in range(len(ys[i])):
				if ys[i][j] == 1:
					grad -= 1/pred[i][j]
					
def erreur_quadratique(xs, ys, predicteur, grad=False):
	'''erreur_quadratique(cs, ys, predicteur) : rend l'erreur quadratique
	de la prédiction des points contenus dans la liste xs par le 
	predicteur, contre les valeurs cibles de ys.'''
	assert classificateur.taille_entree == len(xs[0])
	assert len(xs) == len(ys)
	preds = [classificateur(x) for x in xs]
	erreur = 0
	if isinstance(preds[0]+0., float):
		assert isinstance(ys[0]+0., float)
		for i in range(len(ys)):
			erreur += (preds[i] - ys[i])**2
	else:
		assert len(preds[0]) == len(ys[0])
		for i in range(len(ys)):
			erreur += np.sum((preds[i] - ys[i])**2)
	return erreur / len(ys)
	
			
class Layer:

	def __init__(self, entree, taille_sortie, activation=relu, opts={}):
		if "type" in opts:
			self.type = opts["type"]
		if "activation" in opts:
			self.activation = opts["activation"]
		else:
			self.activation = relu
		self.activation = activation

		if isinstance(entree, Layer):
			self.shape = (entree.shape[-1], taille_sortie)
			self.entree = entree
		elif isinstance(entree, int):
			self.shape = (entree, taille_sortie)
			self.entree = None
		else:
			raise ValueError("Mauvais type d'entrée. Entree : "+str(entree))

		self.synapses = init_mat(self.shape[0], self.shape[1])
		self.biais = init_biais(self.shape[1])

		self.nb_params = (self.shape[0]+1) * self.shape[1]

	def __call__(self, x):
		if self.entree == None:
			res_inter = x
		else:
			res_inter = self.entree(x)
		return self.activation(np.dot(res_inter, self.synapses) + self.biais)

	def get_params(self):
		return np.concatenate((self.synapses.flatten(), self.biais))

	def set_params(self, p):
		assert len(p) == self.nb_params
		self.synapses = p[:self.shape[0]*self.shape[1]].reshape(self.shape)
		self.biais = p[self.shape[0]*self.shape[1]:]

			
class f_erreur():

	def __init__(self, type="entropie_croisee"):
		pass
			
	def grad(self, x):
		pass
				
def init_mat(n,m,type="randn"):
	if type=="randn":
		return 1/np.sqrt(n) * np.random.randn(n,m)

def init_biais(n,type="randn"):
	if type=="randn":
		return 1/np.sqrt(n) * np.random.randn(n)



def mnist_to_data(chemin="./", nom_fichier="mnist_train.csv", nb_pts=np.infty):
	'''mnist_to_data(chemin, nom_fichier, nb_pts) charge les nb_pts premières données mnist 
	situé au chemin chemin (ne pas oublier le '/' à la fin). Rend (xs, ys) où xs correspondent 
	aux images sous formes de vecteurs, et ys est la liste des labels sous forme de [0,0,1,0,...0] 
	(si l'image représente le chiffre 2).'''
	mnist_data = np.loadtxt(chemin+nom_fichier, delimiter=',')
	xs = []
	ys = []
	pos = np.arange(10)
	for d in mnist_data:
		if len(xs) >= nb_pts:
			break
		xs.append(d[1:])
		ys.append((pos == d[0]).astype(np.float))
	return (xs, ys)


def montre_point(x, y=None):
	plt.imshow(x.reshape((28,28)), cmap='gray')
	if y is not None:
		plt.title(str(np.argmax(y)))
