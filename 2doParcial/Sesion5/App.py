# -*- coding: utf-8 -*-

import string
import constants
import random
import os
import re
import io
import subprocess
from   Crypto.Cipher import DES3
from   Crypto        import Random
from   Crypto.Random import random


specialCharacter = constants.CONSTANT_SP
base             = constants.CONSTANT_B
keySize          = constants.CONSTANT_KS
allowKeySize     = constants.CONSTANT_AS
keyFile          = constants.CONSTANT_KF
numberOfSC       = constants.CONSTANT_NSP
writeMode        = constants.CONSTANT_WM
readMode         = constants.CONSTANT_RM
zeroSymbol       = constants.CONSTANT_ZS
multiplus        = constants.CONSTANT_M8
binaryReadM      = constants.CONSTANT_RBM
binaryWriteM     = constants.CONSTANT_BWM
initialMessage   = constants.CONSTANT_IM
ivFile           = constants.CONSTANT_IVF
command1         = constants.CONSTANT_JC
command2         = constants.CONSTANT_RF
command3         = constants.CONSTANT_CC
ivCode           = constants.CONSTANT_IVC
decryptFile_       = constants.CONSTANT_DF

obtainBaseList =  lambda specialCharacter, size: list(string.printable[:base-numberOfSC])

baseList = obtainBaseList(specialCharacter, base)



# UTILITIES

def completeWithZeros(data):
    while len(data) % multiplus != 0:
        data += zeroSymbol
    return data

def completeWithSpecialSymbol(data, symbolToAdd):
    while len(data) % multiplus != 0:
        data += symbolToAdd
    return data

def completeWithFibonacciNumbers(data):
    temporaryList = []
    counter = 0

    for i in range(multiplus-1):
        temporaryList.append(obtainFibonacciNumber(i))

    while(len(data) % multiplus != 0):
        data+=str(temporaryList[counter])
        counter+=1

    return data

def completeWithRandomString(data):
    temporaryList = baseList
    random.shuffle(temporaryList)
    counter = 0
    
    while(len(data) % multiplus != 0):
        data += str.encode(str(temporaryList[counter]))
        counter+=1

    return data

def obtainFibonacciNumber(n):
    if n <= 1:
        return n
    else:
        return(obtainFibonacciNumber(n-1) + obtainFibonacciNumber(n-2))








def obtainKey(keySize):
    key = []
    if keySize in allowKeySize:
        for i in range(keySize):
            key.append(random.choice(baseList))

    return ''.join(key)

def saveDataInFile(data, fileName):
    file = open(fileName, writeMode)
    file.write(data)
    file.close()


def obtainPlainText(fileName):
    file = open(fileName, binaryReadM)
    data = file.read()
    file.close()
    return data

def obtainPadLen(data):
    counter = 0
    while len(data) % multiplus != 0:
        counter+=1
    return counter

def saveBinaryFile(data, fileName):
    file = open(fileName,binaryWriteM)
    file.write(data)
    file.close()

def readFileData(fileName):
    file = open(fileName,readMode)
    data = file.read()
    file.close()
    return data

def encryptFile(fileToEncrypt):
    
    pseudoKey = obtainKey(keySize)
    iv = Random.new().read(DES3.block_size)
    saveBinaryFile(iv, ivFile)
    plainText = obtainPlainText(fileToEncrypt)
    pad_len = obtainPadLen(plainText)
    saveDataInFile(pseudoKey+str(pad_len),keyFile)
    encryptText = des3_encrypt(pseudoKey,iv,plainText)
    myTuple = os.path.splitext(fileToEncrypt)
    saveBinaryFile(encryptText,myTuple[0]+"_"+myTuple[1].replace(".",""))

def decryptFile(fileToDecrypt,keyFile):
    myTuple = extractData(keyFile)
    pseudoKey = myTuple[0]
    pad_len   = int(myTuple[1])
    iv = obtainPlainText(ivFile)
    encryptText = obtainPlainText(fileToDecrypt)
    var = des3_decrypt(pseudoKey,iv,pad_len,encryptText)
    myTuple = os.path.splitext(fileToDecrypt)
    temporaryStr = str(myTuple[0])
    extension = re.findall(r'_.*', temporaryStr)[0].replace("_","")
    saveBinaryFile(var,decryptFile_+"."+extension)


def _make_des3_encryptor(key, iv):
    encryptor = DES3.new(key, DES3.MODE_CBC, iv)
    return encryptor

def des3_encrypt(key, iv, data):
    encryptor = _make_des3_encryptor(key, iv)
    pad_len = multiplus - len(data) % multiplus 
    padding = chr(pad_len) * pad_len 
    data += str.encode(padding)
    return encryptor.encrypt(data)

def des3_decrypt(key, iv, pad_len,data):
    encryptor = _make_des3_encryptor(key, iv)
    result = encryptor.decrypt(data)
    result = result[:len(result)-pad_len]
    return result

def extractData(keyFile):
    data = readFileData(keyFile)
    key = data[:keySize]
    len_pad = data[keySize]

    return key,len_pad

def clearTerminal():
    subprocess.call(command3, shell=True)

def testApp():
    clearTerminal()
    try:
        option = int(input(initialMessage))
        if option == 1:
            clearTerminal()
            fileToEncrypt = str(input("Enter the file to encrypt: "))
            encryptFile(fileToEncrypt)
        elif option == 2:
            clearTerminal()
            fileToDecrypt = str(input("Enter the file to decrypt: "))
            keyFile       = str(input("Enter the file which contains your key: "))
            decryptFile(fileToDecrypt,keyFile)
        else:
            os._exit(0)
    except ValueError:
        os._exit(-1)

    #var = des3_decrypt(pseudoKey,iv,pad_len,encryptText)

    #saveBinaryFile(var,"hdp.txt")

testApp()




"""
key = 'Sixteen byte keydiiiiiii'

iv = Random.new().read(DES3.block_size) #DES3.block_size==8

cipher_encrypt = DES3.new(key, DES3.MODE_OFB, iv)

plaintext = 'sona si latine loqueri  ' #padded with spaces so than len(plaintext) is multiple of 8

encrypted_text = cipher_encrypt.encrypt(plaintext)

print(encrypted_text)

cipher_decrypt = DES3.new(key, DES3.MODE_OFB, iv) #you can't reuse an object for encrypting or decrypting other data with the same key.


cipher_decrypt.decrypt(encrypted_text)

cipher_decrypt.decrypt(encrypted_text) #you cant do it twice
"""
"""
For MODE_ECB, MODE_CBC, and MODE_OFB, plaintext length (in bytes) must be a multiple of block_size.
For MODE_CFB, plaintext length (in bytes) must be a multiple of segment_size/8.
For MODE_CTR, plaintext can be of any length.
For MODE_OPENPGP, plaintext must be a multiple of block_size, unless it is the last chunk of the message.
key size (must be either 16 or 24 bytes long)
"""