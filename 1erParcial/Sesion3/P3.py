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
matrix_size = 3

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
	inverse = np.array([[-1,-1,-1], [-1,-1,-1],[-1,-1,-1]])
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
	gcd = getEuclidean(getDeterminant(matrix))[0]
	if not(gcd == 1):
		errorType = 1
	if fileSize<5 and type_cf:
		errorType = 4 
	return errorType

def convertListToDictionary(myList):
	temporaryList = myList
	temporaryDictionary = {}
	for i in range(specialCases):
		temporaryList.pop()
	for i in range(len(myList)):
		temporaryDictionary[i] = temporaryList[i]  
	return temporaryDictionary

def filterWord(originalWord, alphabet):
	finalString = ""
	temporaryList = list(originalWord)
	for i in range(len(temporaryList)):
		if temporaryList[i] in alphabet.values():
			finalString+=temporaryList[i]
	return finalString

# IMPORTANTE
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
	for i in range(faltantes):
		listOfKeys.append(0)

	for i in range(0,len(listOfKeys),matrix_size):
		auxList = np.array([0,0,0]);
		for j in range(matrix_size):
			auxList[j] = listOfKeys[i+j]
		newKeys = np.dot(auxList,matrix) % sizeAlphabet
		for j in range(len(newKeys)):
			cipherWord+=(alphabet[newKeys[j]])

	return cipherWord


def encryptOrDecryptPlainText(originalText, matrix, sizeAlphabet, alphabet,type_cf):
    arrayOfWords = originalText.split()

    fullText = ""
    for i in range(len(arrayOfWords)):
        fullText += (filterWord(arrayOfWords[i],alphabet))

    cipherText = encryptOrDecryptWord(fullText,alphabet,matrix,type_cf)
	
    return cipherText
# IMPORTANTE
def readMatrixValues(matrixFile):
	sourceFile = matrixFile+".txt"
	values = open(sourceFile, 'r').read()
	a,b,c,d,e,f,g,h,i = values.split()
	matrix = np.array([[int(a),int(b),int(c)],[int(d),int(e),int(f)],[int(g),int(h),int(i)]])
	return matrix

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

def testApp():
	initialFile = "plainText"
	matrixFile = "matrixKey"
	miComando   = "clear"
	subprocess.call(miComando, shell=True)
	option = input("1: Encrypt \n2: Decrypt \nInput: ")
	subprocess.call(miComando, shell=True)
	
	option = int(option)

	if (int(option) == 1):
		encryptOrDecryptFromFile(matrixFile,initialFile ,"cipherText",True)
		os.rename('cipherText.txt',initialFile+".hill")
		print("Message successfully encrypted!")
	elif (option == 2):
		shutil.copyfile(initialFile+'.hill', initialFile+'_.hill')  
		os.rename(initialFile+'.hill',"cipherText.txt")
		os.rename(initialFile+'_.hill',initialFile+'.hill')
		encryptOrDecryptFromFile(matrixFile,"cipherText","decipherText", False)
		os.remove("cipherText.txt")
		print("Decrypting DONE!")
		
#testApp()
# Como sacar a K?
# 1.-Primero necesitamos sacar la matriz del texto plano
# 2.-Despues debemos sacar la inversa de ese texto plano
# 3.- Sacamos la matriz del texto cifrado
# 4.- Para sacar a nuestra K(llave) multiplicamos la Inversa del plano y nuestro cifrado

# Como descifrar un texto cifrado con la K que conseguimos?
# 1.- Sacamos la matriz del texto cifrado
# 2.- Sacamos a la inversa de nuestra k
# 3.- Multiplicamos el cifrado por la inversa
# 4.- Conseguimos el texto original
def prueba():
	plano = np.array([[7,14,11],[0,15,14],[17,17,14]])
	#print(getDeterminant(plano))
	inversa = getMatrixInverse(plano)
	#print(inversa)
	cifrado = np.array([[5,12,14],[18,2,3],[15,1,22]])
	k = np.dot(inversa,cifrado) % sizeAlphabet
	print("La K es")
	print(k)
	perro = np.array([[15,4,17],[17,14,6],[0,19,14]])
	cifrado_perro = np.dot(perro,k)%sizeAlphabet
	print("Cifrado perro")
	print(cifrado_perro)
	inversa_k = getMatrixInverse(k)
	original_perro = np.dot(cifrado_perro,inversa_k)%sizeAlphabet
	print("Orignal perro")
	print(original_perro)

prueba()