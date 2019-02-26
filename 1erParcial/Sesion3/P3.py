# -*- coding: utf-8 -*-
import os
import string
import sys
import subprocess
import shutil
import numpy as np
import math

sizeAlphabet = 94
specialCases = 6
matrix_size = 3




###############################################################################################################################
######################################################### MATRIX STUFF ########################################################
###############################################################################################################################




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






###############################################################################################################################
######################################################## DESCIFRAR ############################################################
###############################################################################################################################




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


# Como descifrar un texto cifrado con la K que conseguimos?
# 1.- Sacamos la matriz del texto cifrado
# 2.- Sacamos a la inversa de nuestra k
# 3.- Multiplicamos el cifrado por la inversa
# 4.- Conseguimos el texto original

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
	# Tambien limpiamos al texto de la matriz
	values = open(sourceFile, 'r').read()
	values = values[1:]
    values = values[:len(values)-1]
	
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

def encryptOrDecryptFromFile(type_cf):

    finalFile = "originalText"
    matrixFile = input("Name of the file with the matrix key:")
    initialFile = input("Name of the file with the ciphertext:")
    sourceFile = initialFile+".txt"
    originalText = open(sourceFile, 'r').read()

    alphabet = convertListToDictionary(list(string.printable))

    # Descomentar esta parte si es que el texto fue generado con el cifrador
    # O quitar las comillas a mano
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





###############################################################################################################################
######################################################## CRIPTOANALYSIS #######################################################
###############################################################################################################################


def getMatrixFromCipherText(text,alphabet,index):
	temporaryList = list(text)
	l = []
	for i in range(len(temporaryList)):
		temporaryString = str(temporaryList[i])
		if temporaryString in alphabet.values():
			lKey = [key for key, value in alphabet.items() if value == temporaryString][0]
			l.append(lKey)

	matrix = np.array([[int(l[index]),int(l[index+1]),int(l[index+2])],[int(l[index+3]),int(l[index+4]),int(l[index+5])],[int(l[index+6]),int(l[index+7]),int(l[index+8])]])
	return matrix

def getMatrixFromPlainText(text,alphabet):
	temporaryList = list(text)
	l = []
	for i in range(len(temporaryList)):
		temporaryString = str(temporaryList[i])
		if temporaryString in alphabet.values():
			lKey = [key for key, value in alphabet.items() if value == temporaryString][0]
			l.append(lKey)
	
	times = len(temporaryList) / (matrix_size*matrix_size)
	offset = matrix_size*matrix_size
	matrix = np.array([[-1,-1,-1], [-1,-1,-1],[-1,-1,-1]])
	final_index = -1
	for i in range(0,times,offset):
		matrix = np.array([[int(l[i]),int(l[i+1]),int(l[i+2])],[int(l[i+3]),int(l[i+4]),int(l[i+5])],[int(l[i+6]),int(l[i+7]),int(l[i+8])]])
		inversa = getMatrixInverse(matrix)
		if(inversa[0][0] != -1):
			final_index = i
			break
	
	return matrix,final_index

# Como sacar a K?
# 1.- Primero necesitamos sacar la matriz del texto plano
# 2.- Despues debemos sacar la inversa de ese texto plano
# 3.- Sacamos la matriz del texto cifrado
# 4.- Para sacar a nuestra K(llave) multiplicamos la Inversa del plano y nuestro cifrado

def computeMatrixKey(originalText,ciphertext,alphabet):
	originalMatrix,index = getMatrixFromPlainText(originalText,alphabet)

	if index == -1:
		print("Could not generate a valid matrix with the given plain text")
		sys.exit()
	
	cipherMatrix = getMatrixFromCipherText(ciphertext,alphabet,index)

	inverseOriginal = getMatrixInverse(originalMatrix)
	matrixKey = np.dot(inverseOriginal,cipherMatrix) % sizeAlphabet

	matrixString = ""
	for i in range(matrix_size):
		for j in range(matrix_size):
			auxString = str(int(matrixKey[i][j]))
			matrixString += (auxString+" ")

	return matrixString

def getMatrixKey():
    plainFile = input("Name of the file with the plain text:")
    cipherFile = input("Name of the file with the ciphertext:")

    originalText = open(plainFile+".txt",'r').read()
    cipherText = open(cipherFile+".txt",'r').read()

    alphabet = convertListToDictionary(list(string.printable))

    arrayOfWords = originalText.split()

    if(len(arrayOfWords) < 9)
    	print("Plain text should be longer")
		sys.exit()
    
    fullText = ""
    for i in range(len(arrayOfWords)):
        fullText += (filterWord(arrayOfWords[i],alphabet))
    # Aqui chance tendremos que llenar el texto plano para poder sacar la matriz de manera adecuada

	# Si leemos un texto cifrado desde archivo debemos limpiarlo
    cipherText = cipherText[1:]
    cipherText = cipherText[:len(cipherText)-1]
    cipherText = cleanCiphertext(cipherText,alphabet)
    cipherText = cleanCiphertext(cipherText,alphabet)

    # Probably gonna have to validate the actual length of the plainText and cipherText
    # For an 3x3 key we need at least a length of 9
    matrixString = repr(computeMatrixKey(fullText,cipherText,alphabet))
    print("Matrix key generated successfully!")
	file = open("matrixKey.txt",'w')
	file.write(str(matrixString))
	file.close()




###############################################################################################################################
########################################################### M A I N ###########################################################
###############################################################################################################################



def initApp():
	miComando   = "clear"
	subprocess.call(miComando, shell=True)
	option = input("1: Get key from given plain text and ciphertext \n2: Decrypt a ciphertext with a given key \nInput: ")
	subprocess.call(miComando, shell=True)
	option = int(option)

	if (int(option) == 1):
		getMatrixKey()
	elif (option == 2):
		encryptOrDecryptFromFile(False)
		print("Deciphering DONE!")

initApp()


# def prueba():
# 	plano = np.array([[7,14,11],[0,15,14],[17,17,14]])
# 	#print(getDeterminant(plano))
# 	inversa = getMatrixInverse(plano)
# 	#print(inversa)
# 	cifrado = np.array([[5,12,14],[18,2,3],[15,1,22]])
# 	k = np.dot(inversa,cifrado) % sizeAlphabet
# 	print("La K es")
# 	print(k)
# 	perro = np.array([[15,4,17],[17,14,6],[0,19,14]])
# 	cifrado_perro = np.dot(perro,k)%sizeAlphabet
# 	print("Cifrado perro")
# 	print(cifrado_perro)
# 	inversa_k = getMatrixInverse(k)
# 	original_perro = np.dot(cifrado_perro,inversa_k)%sizeAlphabet
# 	print("Orignal perro")
# 	print(original_perro)

# def prueba2():
# 	plainText = "HOLAPORRO"
# 	cipherText = "FMOSCDPBW"
# 	alpha = string.printable
# 	alphabet = convertListToDictionary(list(alpha))
# 	print(computeMatrixKey(plainText,cipherText,alphabet))

# #initApp()
# prueba2()