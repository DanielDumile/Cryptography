# Session 3: Cryptanalysis of Hill cipher
# 2.1
# Author: David Josue Rodriguez Chavez
# 02/20/2019

import string
import codecs
from numpy import genfromtxt, linalg, asmatrix, asarray, squeeze, dot, zeros, savetxt, array

#--------------------- INIT FUNCTIONS -----------------------

# Return all multiples of a number until limit (top) as an array:<int>
def multiples(number, top):
    multi = number
    array = []
    while multi < top:
        array.append(multi)
        multi += number
    return array

# Return all prime factors of n as an array:<int>
def prime_factors(n):
    i = 2
    factors = set()
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.add(i)
    if n > 1:
        factors.add(n)
    return list(factors)

# Return Zn array:<int>
def zarray(numbers):
    zn = list(range(1, numbers[0]))
    for x in numbers[1:]:
        for y in multiples(x, numbers[0]):
            if y in zn:
                zn.remove(y)
    print("Zn*" + str(numbers[0]) + ": " + str(zn))
    return zn

# Global variables
alphabet = string.printable[:len(string.printable)-6]
modulo = len(alphabet)
aux = [modulo] + prime_factors(modulo)
zn = zarray(aux)

# -------------------TOOLS------------

# Print matrix
def pmat(matrix):
    matrix = asarray(matrix)
    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in matrix]))

# Extended Euclidean algorithm, return (gcd, x, y):<int>
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

# Modular Multiplicative Inverse (a^-1 mod m), return a^-1:<int mod modulo>
def modinv(a, modulo):
    g, x, y = egcd(a, modulo)
    if g != 1:
        raise Exception('Inverso multiplicativo inexistente')
    else:
        return x % modulo

# ---------------FUNCTIONS---------------------------

# Return adjoint of matrix:<array>
def adjoint(matrix):
    cofactor = linalg.inv(matrix).T * linalg.det(matrix)
    aux = squeeze(asarray(cofactor.transpose()))
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[0]):
            aux[i][j] = round(aux[i][j]%modulo)
    return aux.astype(dtype=int)

# Return inverse of matrix:<array>
def inverse(matrix):
    detinv = modinv(round(linalg.det(matrix))%modulo, modulo)
    adj = adjoint(matrix)
    inverse = (detinv*adj)%modulo
    return inverse.astype(dtype=int)

# Verify key
def kverify(k):
    global det
    det = round(linalg.det(k))%modulo
    print("Det(k) = " + str(det))
    if det in zn:
        return True
    else:
        return False

# Create matrix K
def kmat():
    # Read file
    file = input("K file name: ")
    data = genfromtxt(file + ".csv", dtype=int, delimiter=',')
    print("K matrix:")
    pmat(data)
    # Verify
    if kverify(data):
        inv = inverse(data)
        print("K':")
        pmat(inv)
        print("K*K':")
        pmat((dot(data, inv))%modulo)
        return data, inv
    else:
        raise Exception('Llave no valida')

# Return a cast string:matrix(3x3) <int>
def tomat(word):
    array = zeros((3,3), dtype=int)
    i = 0
    for x in range(0,3):
        for y in range(0, 3):
            array[x][y] = alphabet.find(word[i])
            i += 1
    return array

# Find a valid key form 2 strings, return a valid key:<array>
def findk(plaintext, ciphertext):
    for x in range(0, len(plaintext), 9):
        mmat = tomat(plaintext[x:x+9])
        print("Mmat:")
        pmat(mmat)
        cmat = tomat(ciphertext[x:x+9])
        print("Cmat:")
        pmat(cmat)
        if kverify(mmat):
            invm = inverse(mmat)
            return dot(invm, cmat)%modulo
    raise Exception("Cannot find a valid key")


#-------------------- CIPHER FUNCTIONS ----------------------

def cipher(k, word):
    aux = k.shape[0] - len(word)%k.shape[0]
    if(aux != 3):
        for x in range(aux):
            word += " "
    ciphered_word = ""
    for x in range(0, len(word), k.shape[0]):
        aux = word[x:x + k.shape[0]]
        auxList = zeros((1, k.shape[0]), dtype=int)
        y = 0
        for y in range(k.shape[0]):
            # print("'" + aux + "'")
            auxList[0][y] = alphabet.find(aux[y])
        cipherList = dot(auxList, k)%modulo
        y = 0
        for y in range(k.shape[0]):
            ciphered_word += alphabet[cipherList[0][y]]
    return ciphered_word

def decipher(k, word):
    deciphered_word = ""
    for x in range(0, len(word), k.shape[0]):
        aux = word[x:x+k.shape[0]]
        auxList = zeros((1, k.shape[0]), dtype=int)
        y = 0
        print("'" + aux + "'")
        for y in range(k.shape[0]):
            auxList[0][y] = alphabet.find(aux[y])
        decipherList = dot(auxList, k)%modulo
        y = 0
        for y in range(k.shape[0]):
            deciphered_word += alphabet[decipherList[0][y]]
    return deciphered_word

# ----------------------- MAIN -----------------------------------
def main():
    option = ""
    while option != "E":
        option = input("[A]nalyze, [C]ipher, [D]ecipher, [E]xit: ").upper()
        if option == "A":
            
            # Read Plaintext
            file = input("Plaintext file name: ")
            plaintext = ""
            with codecs.open(file + ".txt", 'r', encoding="utf-8") as data:
                plaintext = data.read()
            new = ""
            for x in range(0, len(plaintext)):
                if plaintext[x] not in set(string.printable[len(string.printable)-6:]):
                    new += plaintext[x]
            plaintext = new
            # Read Ciphertext
            file = input("Ciphertext file name: ")
            ciphertext = ""
            with codecs.open(file + ".afn", 'r', encoding="utf-8") as data:
                ciphertext = data.read()
            
            # Search for a valid key
            anak = findk(plaintext, ciphertext)

            print("Analysis key:")
            pmat(anak)
            savetxt('analysis_key.csv', anak, fmt='%i', delimiter=',')
            print("Key saved as analysis_key.csv")
        elif option == "C":
            k, kinv = kmat()
            file = input("Data file name: ")
            data = ""
            with codecs.open(file + ".txt", 'r', encoding="utf-8") as plaintext:
                data = plaintext.read()
                # print(data)
            new = ""
            for x in range(0, len(data)):
                if data[x] not in set(string.printable[len(string.printable)-6:]):
                    new += data[x]
            data = new
            with codecs.open(file + ".afn", 'w', encoding="utf-8") as ciphered_text:
                ciphered_text.write(cipher(k, data))
        elif option == "D":
            k, kinv = kmat()
            file = input("Data file name: ")
            data = ""
            with codecs.open(file + ".afn", 'r', encoding="utf-8") as plaintext:
                data = plaintext.read()
            with codecs.open(file + ".txt", 'w', encoding="utf-8") as deciphered_text:
                deciphered_text.write(decipher(kinv, data))

if __name__ == '__main__':
    main()