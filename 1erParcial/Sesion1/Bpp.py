# -*- coding: utf-8 -*-
import os
import string
import sys
import subprocess
import shutil
# El problema es que al momento de leer el codigo es solo una palabra, entonces los modulos no los hace bien

sizeAlphabet = 94
specialCases = 6
index_total= 0

def validateValues(fileSource, type_cf):
	errorType = 0
	factor = 0.001
	fileSize = int(os.path.getsize(fileSource+".txt"))*factor
	if fileSize<5 and type_cf:
		errorType = 4 
	return errorType

#Se queda sin modificaciones
def convertListToDictionary(myList):
	temporaryList = myList
	temporaryDictionary = {}
	for i in range(specialCases):
		temporaryList.pop()
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


def encryptOrDecryptWord(originalWord, alphabet,filteredKey,type_cf):
	#Cadena con el resultado de la operacion
	cipherWord = ""

	#Quitamos el primer y el ultimo caracter si es que vamos a descifrar
	if type_cf == False:
		originalWord = originalWord[1:]
		originalWord = originalWord[:len(originalWord)-1]

	#Convertimos la palabra a lista y sacamos sus llaves correspondientes
	temporaryList = list(originalWord)
	listOfKeys = []
	#Convertimos la llave a lista y sacamos sus llaves correspondientes
	keyAuxList = list(filteredKey)
	arrayKey = []
	
	#Sirve para sacar las llaves de la palabra original
	for i in range(len(temporaryList)):
		temporaryString = str(temporaryList[i])
		if temporaryString in alphabet.values():
			#Supongo que de aqui se saca el valor de la posicion
			lKey = [key for key, value in alphabet.items() if value == temporaryString][0]
			listOfKeys.append(lKey)

	#Ahora sacamos las llaves de la key
	for i in range(len(keyAuxList)):
		auxKey = str(keyAuxList[i])
		if auxKey in alphabet.values():
			lKey2 = [key for key, value in alphabet.items() if value == auxKey][0]
			arrayKey.append(lKey2)

	size_key = int(len(keyAuxList))
	n = int(len(alphabet))

	index = 0
	global index_total

	saltamos = False
	for j in range(len(listOfKeys)):
		index_total %= size_key

		if saltamos == True:
			saltamos = False
			continue

		oldKey = int(listOfKeys[j])
		indexKey = int(arrayKey[index_total])
		
		if oldKey == 85:
			siguiente = oldKey = int(listOfKeys[j+1])
			saltamos = True
			if siguiente == 85:
				oldKey = 85
			else:# Si no es otro \ entonces es comilla que es 68
				oldKey = 68
		
		#Si vamos a encriptar
		if type_cf == True:
			newKey = (oldKey + indexKey ) % n
		else:#Si vamos a desencriptar
			newKey = (oldKey - indexKey) % n
		newKey = int(newKey)
		#Sacamos la nueva llave y sacamos el caracter correspondiente del alfabeto		
		cipherWord += str(alphabet[newKey])
		index_total+=1

	return cipherWord


def encryptOrDecryptPlainText(originalText, key, sizeAlphabet, type_cf):
    #Arreglo con todas las palabras del texto
    arrayOfWords = originalText.split()
    #El alfabeto a usar
    alphabet = convertListToDictionary(list(string.printable))
    #El texto resultante
    cipherText = ""
    #Por cada palabra en nuestro texto
    filteredKey = filterWord(key,alphabet)
    for i in range(len(arrayOfWords)):
	    filteredWord = filterWord(arrayOfWords[i],alphabet)
	    cipherText  += (encryptOrDecryptWord(filteredWord,alphabet,filteredKey,type_cf))
    return cipherText

def askKey():
	key = input("Enter the key: ")
	return key

def encryptOrDecryptFromFile(initialFile, finalFile, type_cf):

    sourceFile = initialFile+".txt"
    #Leemos todos los valores
    originalText = open(sourceFile, 'r').read()

    #Leemos la llave a usar
    keyValue = askKey()

    #Esto se queda
    #errorType = validateValues(initialFile, type_cf)
    errorType = 0
    #Nos muestra el error pertinente
    if errorType > 0:
    	print("Error "+str(errorType)+" has been made, see the documentation")
    	sys.exit()
    else:
    	#aqui ya va la parte del cifrado o descifrado
	    cipherText = repr(encryptOrDecryptPlainText(originalText, keyValue, sizeAlphabet,type_cf))
	    #Creamos el nuevo archivo
	    file = open(finalFile+".txt",'w')
	    #Escribimos en el
	    file.write(str(cipherText))
	    file.close()

def testApp():

	initialFile = "plainText"
	miComando   = "cls"
	subprocess.call(miComando, shell=True)
	option = input("1: Encrypt \n2: Decrypt \nInput: ")
	#subprocess.call(miComando, shell=True)
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

testApp()