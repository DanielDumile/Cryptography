# -*- coding: utf-8 -*-
import os
import string
import sys
import subprocess
import shutil


sizeAlphabet = 94
specialCases = 6


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

def validateValues(numberA, numberB, sizeAlphabet,mcd, fileSource, type_cf):
	numberA = int(numberA)
	numberB = int(numberB)
	sizeAlphabet = int(sizeAlphabet)
	mcd = int(mcd)
	errorType = 0
	factor = 0.001

	fileSize = int(os.path.getsize(fileSource+".txt"))*factor

	if not( numberB >= 0 and numberB <= sizeAlphabet ):
		errorType = 1
	
	if not( numberA != 0 and numberA >= 1 ):
		errorType = 2
	
	if not( mcd == 1 ):
		errorType = 3

	return errorType


def filterWord(originalWord, alphabet):

	finalString = ""
	temporaryList = list(originalWord)
	for i in range(len(temporaryList)):
		if temporaryList[i] in alphabet.values():
			finalString+=temporaryList[i]
	return finalString


def convertListToDictionary(myList):

	temporaryList = myList
	temporaryDictionary = {}

	for i in range(specialCases):
		temporaryList.pop()

	for i in range(len(myList)):
		temporaryDictionary[i] = temporaryList[i]  

	return temporaryDictionary

def encryptOrDecryptPlainText(originalText, numberA, numberB, sizeAlphabet,tupleValuesGCD, type_cf):
    arrayOfWords = originalText.split()
    alphabet = convertListToDictionary(list(string.printable))
    cipherText = ""

    for i in range(len(arrayOfWords)):
	    filteredWord = filterWord(arrayOfWords[i],alphabet)
	    cipherText  += (encryptOrDecryptWord(filteredWord,alphabet,numberA,numberB,tupleValuesGCD, type_cf))

    return cipherText


def encryptOrDecryptWord(originalWord, alphabet,numberA,numberB,tupleValuesGCD,type_cf):
	
	cipherWord    = ""
	temporaryList = list(originalWord)
	listOfKeys    = []
	
	for i in range(len(temporaryList)):
		temporaryString = str(temporaryList[i])
		if temporaryString in alphabet.values():
			lKey = [key for key, value in alphabet.items() if value == temporaryString][0]
			listOfKeys.append(lKey)
	
	for j in range(len(listOfKeys)):
		n = int(len(alphabet))
		oldKey = int(listOfKeys[j])
		numberB = int(numberB)
		numberA = int(numberA)
		if type_cf == True:
			newKey = int((oldKey*numberA+numberB)) % n
		else:
			tupleaux = int(tupleValuesGCD[1])
			otheraux = int((oldKey-numberB))
			newKey = int((tupleaux*otheraux)) % n
		newKey = int(newKey)			
		cipherWord +=str(alphabet[newKey])
	return cipherWord


def askValues():
    numberA = input("Enter decimation   constant  (a) * a = { a ϵ P | a != 2 } : ")
    numberB = input("Enter displacement constant  (b) * b = { b ϵ N | b >= 0 and b <= 94 } : ")
    return numberA, numberB


def encryptOrDecryptFromFile(initialFile, finalFile, type_cf):

    sourceFile = initialFile+".txt"
    #print(sourceFile)
    originalText = open(sourceFile, 'r').read()    
    #print(originalText)
    tupleValues = askValues() 
    numberA = tupleValues[0] 
    numberB = tupleValues[1]
    tupleValuesGCD = extendedEuclideanA(numberA, sizeAlphabet)
    errorType = validateValues(numberA,numberB,sizeAlphabet,tupleValuesGCD[0], initialFile, type_cf)
    
    if errorType > 0:
    	print("Error "+str(errorType)+" has been made, see the documentation")
    	sys.exit()
    else:
	    cipherText = repr(encryptOrDecryptPlainText(originalText, numberA, numberB, sizeAlphabet, tupleValuesGCD,type_cf))
	    file = open(finalFile+".txt",'w')
	    file.write(cipherText)
	    file.close()

def testApp():

	initialFile = "plainText"
	miComando   = "cls"
	
	subprocess.call(miComando, shell=True)

	option = input("1: Encrypt \n2: Decrypt \nInput: ")
	
	subprocess.call(miComando, shell=True)
	#print(option)
	option = int(option)
	if (int(option) == 1):
		#print("option")
		encryptOrDecryptFromFile(initialFile ,"cipherText"  , True )
		os.rename('cipherText.txt',initialFile+".afn")
	elif (option == 2):
		shutil.copyfile(initialFile+'.afn', initialFile+'_.afn')  
		os.rename(initialFile+'.afn',"cipherText.txt")
		os.rename(initialFile+'_.afn',initialFile+'.afn')
		encryptOrDecryptFromFile("cipherText","decipherText", False)
		os.remove("cipherText.txt")

testApp()