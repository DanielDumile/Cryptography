# -*- coding: utf-8 -*-
import os
import string
import sys
import subprocess
import shutil
import numpy as np
import math

 #Instituto Politecnico Nacional
 #Escuela Superior de Computo
 #Cryptography
 #Group: 3CM6
 #Student: Gonzalez Nunez Daniel
 #Teacher: Dra. Diaz Santiago Sandra
 #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
 #Hill Cipher
 #Date: 20/02/2019
 
# Inicializacion de variables globales importantes
sizeAlphabet = 94
specialCases = 6
matrix_size = 3

# COSAS DE MATRICES

# Funcion que recibe dos numeros enteros como parametro y regresa los valoresde
# gcd(A,B)
# x: ax+by = gcd(a,b)
# y: ax+by = gcd(a,b)

def extendedEuclideanA(numberA,numberB):
	numberA = int(numberA)
	numberB = int(numberB)
	if numberB != 0:
		u0 = 1
		u1 = 0
		v0 = 0
		v1 = 1
		while numberB != 0:
			residue  = int(numberA) % int(numberB)
			quotient = (numberA - residue)/numberB
			u        = u0 - quotient * u1
			v        = v0 - quotient * v1
			numberA  = numberB
			numberB  = residue
			u0       = u1
			u1       = u
			v0       = v1
			v1       = v
		return numberA,u0,v0
	else:
		return 0,1,0
# Función que recibe como parametro una matriz de NxN y regresa el determinante de esa matriz, modulo el tamaño de nuestro alfabeto

def getDeterminant(matrix):
	return round(np.linalg.det(matrix) % sizeAlphabet) 
# Función que recibe como parámetro una matriz de NxN y regresa la matriz adjunta.
# La matriz adjunta se define como la matriz transpuesta del producto del determinante y la matriz de cofactores

def getAdjoint(matrix):
    cofactor = np.linalg.inv(matrix).T * np.linalg.det(matrix)
    aux = cofactor.transpose()
    for i in range(matrix_size):
    	for j in range(matrix_size):
    		aux[i][j] = round(aux[i][j]%sizeAlphabet)
    return aux

# Funcion que regresa el gcd de un entero y el tamaño de nuestro alfabeto, así como el inverso modular de ese número.

def getEuclidean(a):
	tupleValues = extendedEuclideanA(a,sizeAlphabet)
	return tupleValues[0],tupleValues[1]

# Función que recibe como parámetro ua matriz de 3x3 y retorna la inversa de dicha matriz

def getMatrixInverse(matrix):
	inverse = np.array([[-1,-1,-1], [-1,-1,-1],[-1,-1,-1]])
	determinant = getDeterminant(matrix)
	gcd,multiplicativeInverse = getEuclidean(determinant)
	if gcd == 1:
		adjoint = getAdjoint(matrix)
		inverse = (multiplicativeInverse*adjoint)%sizeAlphabet
	return inverse

#COSAS PARA ARCHIVOS

# Función usada para validar los valores de la matriz.
# Si el gcd del determinante de la matriz y el alfabeto es diferente de 1, la matriz no es válida.

def validateValues(matrix, fileSource, type_cf):
	errorType = 0
	factor = 0.001
	fileSize = int(os.path.getsize(fileSource+".txt"))*factor
	gcd = getEuclidean(getDeterminant(matrix))[0]
	if not(gcd == 1):
		errorType = 1
	# if fileSize<5 and type_cf:
	# 	errorType = 4 
	return errorType

# Función que recibe una lista de caracteres y nos regresa un diccionario con esos caracteres

def convertListToDictionary(myList):
	temporaryList = myList
	temporaryDictionary = {}
	for i in range(specialCases):
		temporaryList.pop()
	for i in range(len(myList)):
		temporaryDictionary[i] = temporaryList[i]  
	return temporaryDictionary

# Función que filtra los caracteres válidos de una palabra

def filterWord(originalWord, alphabet):
	finalString = ""
	temporaryList = list(originalWord)
	for i in range(len(temporaryList)):
		if temporaryList[i] in alphabet.values():
			finalString+=temporaryList[i]
	return finalString

# Función que recibe un texto, una matriz llave y una bandera que indica la operacion a realizar.
# Si la bandera indica que descifraremos, calcularemos la inversa de la matriz obtenida 

def encryptOrDecryptWord(originalWord, alphabet,matrix,type_cf):
	cipherWord = ""

	if type_cf == False:
		matrix = getMatrixInverse(matrix)

	temporaryList = list(originalWord)
	listOfKeys = []
	
	for i in range(len(temporaryList)):
		temporaryString = str(temporaryList[i])
		if temporaryString in alphabet.values():
			lKey = [key for key, value in alphabet.items() if value == temporaryString][0]
			listOfKeys.append(lKey)

	faltantes = len(listOfKeys) % matrix_size
	print(faltantes)
	if(faltantes > 0):
		for i in range(matrix_size-faltantes):
			listOfKeys.append(0)

	for i in range(0,len(listOfKeys),matrix_size):
		auxList = np.array([0,0,0]);
		for j in range(matrix_size):
			auxList[j] = listOfKeys[i+j]
		newKeys = np.dot(auxList,matrix) % sizeAlphabet
		for j in range(len(newKeys)):
			cipherWord+=(alphabet[newKeys[j]])

	return cipherWord

# Funcion que recibe el texto plano y genera una sola palabra concatenando todo el texto

def encryptOrDecryptPlainText(originalText, matrix, sizeAlphabet, alphabet,type_cf):
    arrayOfWords = originalText.split()

    fullText = ""
    for i in range(len(arrayOfWords)):
        fullText += (filterWord(arrayOfWords[i],alphabet))

    cipherText = encryptOrDecryptWord(fullText,alphabet,matrix,type_cf)
	
    return cipherText
# Función que abre el archivo seleccionado para poder leer los valores de la matriz introducida por el usuario.

def readMatrixValues(matrixFile):
	sourceFile = matrixFile+".txt"
	values = open(sourceFile, 'r').read()
	a,b,c,d,e,f,g,h,i = values.split()
	matrix = np.array([[int(a),int(b),int(c)],[int(d),int(e),int(f)],[int(g),int(h),int(i)]])
	return matrix

# Función usada para quitar los carácteres que causan problemas a Python

def cleanCiphertext(cipherText,alphabet):
	cleanText = ""
	saltar = True
	for i in range(len(cipherText)):
		temporaryString = str(cipherText[i])
		if temporaryString in alphabet.values():
			lKey = [key for key, value in alphabet.items() if value == temporaryString][0]
			if lKey == 85:
				if saltar == True:
					saltar = False
					continue
				else:
					saltar = True
			if lKey == 68:
				saltar = True
			cleanText+=temporaryString

	return cleanText

# Funcion que abre un archivo a cifrar o descifirar y valida los valores introducidos por el usuario.
# Dependiendo de la acción a realizar, se limpia el texto o no.

def encryptOrDecryptFromFile(matrixFile,initialFile, finalFile, type_cf):
    sourceFile = initialFile+".txt"
    originalText = open(sourceFile, 'r').read()

    alphabet = convertListToDictionary(list(string.printable))

    if type_cf == False:
        originalText = originalText[1:]
        originalText = originalText[:len(originalText)-1]
        originalText = cleanCiphertext(originalText,alphabet)

    matrix = readMatrixValues(matrixFile)
    errorType = validateValues(matrix,initialFile, type_cf)

    if errorType > 0:
    	print("Error "+str(errorType)+" has been made, see the documentation")
    	sys.exit()
    else:
	    cipherText = repr(encryptOrDecryptPlainText(originalText, matrix, sizeAlphabet,alphabet,type_cf))
	    file = open(finalFile+".txt",'w')
	    file.write(str(cipherText))
	    file.close()
# Funcion principal
def testApp():
	initialFile = "plainText"
	miComando   = "clear"
	subprocess.call(miComando, shell=True)
	option = input("1: Encrypt \n2: Decrypt \nInput: ")
	subprocess.call(miComando, shell=True)
	
	option = int(option)
	matrixFile = input("Name of the file that contains the key:")

	if (int(option) == 1):
		encryptOrDecryptFromFile(matrixFile,initialFile ,"cipherText",True)
		os.rename('cipherText.txt',initialFile+".hill")
		print("Message successfully ciphered!")
	elif (option == 2):
		shutil.copyfile(initialFile+'.hill', initialFile+'_.hill')  
		os.rename(initialFile+'.hill',"cipherText.txt")
		os.rename(initialFile+'_.hill',initialFile+'.hill')
		encryptOrDecryptFromFile(matrixFile,"cipherText","decipherText", False)
		os.remove("cipherText.txt")
		print("Deciphering DONE!")
		
testApp()