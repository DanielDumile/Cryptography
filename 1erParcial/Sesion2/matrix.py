# -*- coding: utf-8 -*-
import os
import string
import sys
import subprocess
import shutil
import numpy as np
import math

sizeAlphabet = 26
specialCases = 6
matrix_size = 2



# COSAS DE MATRICES





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

def getDeterminant(matrix):
	return round(np.linalg.det(matrix) % sizeAlphabet) 

def getAdjoint(matrix):
    cofactor = np.linalg.inv(matrix).T * np.linalg.det(matrix)
    aux = cofactor.transpose()
    for i in range(matrix_size):
    	for j in range(matrix_size):
    		aux[i][j] = round(aux[i][j]%sizeAlphabet)
    return aux

def getEuclidean(a):
	tupleValues = extendedEuclideanA(a,sizeAlphabet)
	return tupleValues[0],tupleValues[1]

def getMatrixInverse(matrix):
	#inverse = np.array([[-1,-1,-1], [-1,-1,-1],[-1,-1,-1]])
	inverse = np.array([[-1,-1], [-1,-1]])
	determinant = getDeterminant(matrix)
	gcd,multiplicativeInverse = getEuclidean(determinant)
	if gcd == 1:
		adjoint = getAdjoint(matrix)
		inverse = (multiplicativeInverse*adjoint)%sizeAlphabet
	return inverse







#COSAS PARA ARCHIVOS





def validateValues(matrix, fileSource, type_cf):
	errorType = 0
	factor = 0.001
	fileSize = int(os.path.getsize(fileSource+".txt"))*factor
	#Debemos validar que el gcd del determinante y el alfabeto sea 1
	gcd = getEuclidean(getDeterminant(matrix))[0]
	if not(gcd == 1):
		errorType = 1
	if fileSize<5 and type_cf:
		errorType = 4 
	return errorType


#Se queda sin modificaciones
def convertListToDictionary(myList):
	temporaryList = myList
	temporaryDictionary = {}
	#for i in range(specialCases):
	#	temporaryList.pop()
	for i in range(len(myList)):
		temporaryDictionary[i] = temporaryList[i]  
	return temporaryDictionary

#Creo que solo checa si los caracteres son validos o nel
def filterWord(originalWord, alphabet):
	finalString = ""
	temporaryList = list(originalWord)
	for i in range(len(temporaryList)):
		if temporaryList[i] in alphabet.values():
			finalString+=temporaryList[i]
	return finalString


def encryptOrDecryptWord(originalWord, alphabet,matrix,type_cf):
	#Cadena con el resultado de la operacion
	cipherWord = ""

	#Si vamos a descifrar entonces usamos la inversa de la matriz
	if type_cf == False:
		matrix = getMatrixInverse(matrix)

	#Convertimos la palabra a lista y sacamos sus llaves correspondientes
	temporaryList = list(originalWord)
	listOfKeys = []
	
	#Sirve para sacar las llaves de la palabra original
	for i in range(len(temporaryList)):
		temporaryString = str(temporaryList[i])
		if temporaryString in alphabet.values():
			lKey = [key for key, value in alphabet.items() if value == temporaryString][0]
			listOfKeys.append(lKey)

	faltantes = len(listOfKeys) % matrix_size

	#Anadimos caracteres faltantes como As
	for i in range(faltantes):
		listOfKeys.append(0)

	# Proceso para multiplicar
	for i in range(0,len(listOfKeys),matrix_size):
		auxList = np.array([0,0]);
		#Copiamos matrix_size elementos de la lista de llaves
		for j in range(matrix_size):
			auxList[j] = listOfKeys[i+j]
		#Sacamos nuestras nuevas llaves mediante la multiplicacion
		newKeys = np.dot(auxList,matrix) % sizeAlphabet
		for j in range(len(newKeys)):
			cipherWord+=(alphabet[newKeys[j]])

	return cipherWord


def encryptOrDecryptPlainText(originalText, matrix, sizeAlphabet, type_cf):
    #Arreglo con todas las palabras del texto
    arrayOfWords = originalText.split()

    #El alfabeto a usar
    #string.printable
    alphabet = convertListToDictionary(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    
    #El texto resultante
    fullText = ""
    
    #Armamos un texto enorme con todas las palabras concatenadas
    for i in range(len(arrayOfWords)):
        fullText += (filterWord(arrayOfWords[i],alphabet))

    cipherText = encryptOrDecryptWord(fullText,alphabet,matrix,type_cf)
	
    return cipherText

def readMatrixValues():
	values = input("Introduce the matrix values: ")
	a,b,c,d = values.split()
	matrix = np.array([[int(a),int(b)],[int(c),int(d)]])
	return matrix

def encryptOrDecryptFromFile(initialFile, finalFile, type_cf):
    sourceFile = initialFile+".txt"
    originalText = open(sourceFile, 'r').read()

    # Solo poner esto cuando se esta leyendo directamente desde un archivo
    # Quitamos el primer y el ultimo caracter si es que vamos a descifrar
    # if type_cf == False:
    #     originalText = originalText[1:]
    #     originalText = originalText[:len(originalText)-1]

    #Creamos nuestra matriz que usaremos
    matrix = readMatrixValues()
    errorType = validateValues(matrix,initialFile, type_cf)

    #Nos muestra el error pertinente
    if errorType > 0:
    	print("Error "+str(errorType)+" has been made, see the documentation")
    	sys.exit()
    else:
    	#aqui ya va la parte del cifrado o descifrado
	    cipherText = repr(encryptOrDecryptPlainText(originalText, matrix, sizeAlphabet,type_cf))
	    #Creamos el nuevo archivo
	    file = open(finalFile+".txt",'w')
	    #Escribimos en el
	    file.write(str(cipherText))
	    file.close()

def testApp():
	initialFile = "plainText"
	miComando   = "clear"
	subprocess.call(miComando, shell=True)
	option = input("1: Encrypt \n2: Decrypt \nInput: ")
	subprocess.call(miComando, shell=True)
	
	option = int(option)

	if (int(option) == 1):
		encryptOrDecryptFromFile(initialFile ,"cipherText",True)
		os.rename('cipherText.txt',initialFile+".afn")
		print("Successful hashing!")
	elif (option == 2):
		shutil.copyfile(initialFile+'.afn', initialFile+'_.afn')  
		os.rename(initialFile+'.afn',"cipherText.txt")
		os.rename(initialFile+'_.afn',initialFile+'.afn')
		encryptOrDecryptFromFile("cipherText","decipherText", False)
		os.remove("cipherText.txt")
		print("Decrypting DONE!")

def prueba():
	matrix = readMatrixValues()
	#matrix = np.array([[11,8],[3,7]])
	#matrix = getMatrixInverse(matrix)
	res = encryptOrDecryptPlainText("JULY",matrix,sizeAlphabet,True)
	print(res)
	#print(getMatrixInverse(matrix))

prueba()
