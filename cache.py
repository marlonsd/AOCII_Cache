#coding: utf-8

class Cache():

	validade = [[]]
	tag = [[]]
	sets = 0
	blocos = 0

	def __init__(self, nsets, assoc):
		self.sets = nsets
		self.blocos = assoc

		for i in range(nsets):
			self.validade[i] += [False]*assoc
			self.tag[i] += [-1]*assoc
			if (i < nsets):
				self.validade += [[]]
				self.tag += [[]]	

	def __done__(self):
		self.validade = []
		self.tag = []
		self.nsets = 0
		self.blocos = 0

	def setCache(self, tag, indice, set):
		self.validade[indice][set] = True
		self.tag[indice][set] = tag

	def getTag(self, indice, set):
		return self.tag[indice][set]

	def getValidade(self, indice, set):
		return self.validade[indice][set]

	def printCache(self):

		for i in range(self.sets):
			for j in range (self.blocos):
				print self.tag[i][j],
			print

class Misses():

	compulsorio = 0
	capacidade = 0
	conflito = 0

	def __init__(self):
		self.compulsorio = 0
		self.capacidade = 0
		self.conflito = 0

	def __done__(self):
		self.compulsorio = 0
		self.capacidade = 0
		self.conflito = 0

	def incMissCompulsorio(self):
		self.compulsorio += 1

	def incMissCapacidade(self):
		self.capacidade += 1

	def incMissConflito(self):
		self.conflito += 1

	def getMissCompulsorio(self):
		return self.compulsorio

	def getMissCapacidade(self):
		return self.capacidade

	def getMissConflito(self):
		return self.conflito

	def printMiss(self):
		i = 0
		print "Miss Compulsório: ", self.compulsorio
		print "Miss Capacidade: ", self.capacidade
		print "Miss Conflito: ", self.conflito
