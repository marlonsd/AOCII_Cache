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

# Arquivo texto
try:
	op = open(nomeArquivo, 'rb') # Arquivo binário
except IOError:
	print "Erro ao abrir o arquivo ", nomeArquivo
	sys.exit(1)


vetor = []
op.seek(0,2)
tamanho = op.tell()
op.seek(0)

while (op.tell() < tamanho):
	r = op.read(4)
	r = "".join("%02x" % ord(c) for c in r)
	vetor += [int(r,16)]

nbits_offset = int(math.log(bsize, 2)); #Log2
nbtis_indice = int(math.log(float(nsets/assoc), 2));

miss = Misses()
hit = 0

print vetor

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
miss.printMiss()
print "Hit: ", hit
