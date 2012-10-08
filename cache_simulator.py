#coding: utf-8

"""
	cache_simulator <nsets> <bsize> <assoc> arquivo_entrada 
		<nsets> x <bsize> x <assoc> = Tamanho da cache
	 	<assoc> = 1 - cache direta
"""

""" Import """

import sys
import math
import random
from cache import Cache
from cache import Misses

""" Funções """

def leituraArquivo(dado):
	i = 0
	lista = []
	string = ''
	check = False

	while(i < len(dado)):

		if dado[i] >= '0' and dado[i] <= '9':
			string += dado[i]
			check = True
		else:
			if check:
				check = False
				lista += [int(string)]
				string = ''

		i += 1

	if check:
		lista += [int(string)]

	return lista

def checkAllValidade(cache, indice, assoc):
	i = 0

	while (i < assoc):
		if (cache.getValidade(indice,i)):
			return True
		i += 1

	return False

def chooseBloco(cache, indice, assoc):
	i = 0

	while (i < 0):
		if (not cache.getValidade(indice,i)):
			return i
		i += 1

	return random.randint(0,assoc - 1)

def checkAllTag(cache, indice, assoc, tag):
	i = 0

	while (i < assoc):
		if (cache.getTag(indice,i) == tag):
			return True
		i += 1

	return False


""" Main """

if len(sys.argv) != 5: # 4 arguementos de fato, mais o nome do arquivo.
	print "Número de parêmetros de entrada menos que o esperad."
	print "cache_simulator <nsets> <bsize> <assoc> arquivo_entrada"
	print
	sys.exit()

nsets = int(sys.argv[1])
bsize = int(sys.argv[2])
assoc = int(sys.argv[3])
nomeArquivo = sys.argv[4]

print nsets, bsize, assoc, nomeArquivo

cache = Cache(nsets, assoc)

# temp = open(nomeArquivo, 'r') # Arquivo texto
try:
	temp = open(nomeArquivo, 'rb') # Arquivo binário
	dado = temp.read()
	temp.close()
except IOError:
	print "Erro ao abrir o arquivo ", nomeArquivo
	sys.exit(1)


vetor = leituraArquivo(dado)

#vetor = [4, 4, 5, 24, 30, 1, 2]

nbits_offset = int(math.log(bsize, 2)); #Log2
nbtis_indice = int(math.log(float(nsets/assoc), 2));

miss = Misses()
hit = 0

print vetor

#cache.printCache()

for i in range (len(vetor)):
	endereco = vetor[i]
	indice = (endereco >> nbits_offset) & (nsets - 1)
	tag = endereco >> (nbits_offset + nbtis_indice)
	print endereco, "- ",
	if (not checkAllValidade(cache, indice, assoc)):
		miss.incMissCompulsorio()
		bloco = chooseBloco(cache, indice, assoc)
		print bloco, " ", tag, " ",
		cache.setCache(tag, indice, bloco) #Mudar
		print "Miss compulsório"

	else:
		if (checkAllTag(cache, indice, assoc, tag)):
				hit += 1
				print "Hit"
		else:
			bloco = chooseBloco(cache, indice, assoc)
			print bloco, " ", tag, " ",
			if (assoc == nsets):
				miss.incMissCapacidade()
				print "Miss Capacidade"
			else:
				miss.incMissConflito()
				print "Miss Conflito"

			#cache.setCache(tag, indice, assoc - 1) #Mudar
			cache.setCache(tag, indice, chooseBloco(cache, indice, assoc))

print
print "Miss Compulsório: ", miss.getMissCompulsorio()
print "Miss Capacidade: ", miss.getMissCapacidade()
print "Miss Conflito: ", miss.getMissConflito()
print "Hit: ", hit