import math
#mod = 100011010
#mod = int(pow(2,8)+pow(2,4)+pow(2,3)+pow(2,1)+pow(2,0))

def basic(b,mod):
    ult = int(math.log2(mod))
    #print("El ultimo es "+str(ult))
    flag = False
    b = b << 1
    #print(getString(b))
    if (b&(1<<ult)):
        #print("Esta prendido el ultimo")
        b = b ^ (1<<ult)
        #print(getString(b))
        #print("Despues del XOR nos da "+ str(b))
        b = b^(mod^(1<<ult))
    return b
    
def mul(a,b,mod):
    tam = int(math.log2(a))+1
    i = 0
    res = 0
    while (i < tam):
        if(a &(1<<i)):
            aux = b
            for j in range(i):
                aux = basic(aux,mod)
            res = res ^ aux
        i= i+1
    return res

def getPoly(s):
    tam = int(len(s))
    res = ""
    for i in range(tam):
        if(s[i] == '1'):
            pos = tam-i-1
            if(pos == 1):
                res+=("x+")
            elif(pos == 0):
                res+="1+"
            else:
                res += ("x^" + str(tam-i-1) + "+")
    return res[0:len(res)-1]

def getNumber(s):
    tam = int(len(s))
    ans = 0
    for i in range(tam):
        if(s[i] == '1'):
            pos = tam-i-1
            ans += pow(2,pos)
    return ans

def getString(a):
    tam = int(math.log2(a))+1
    ans = ""
    for i in range(tam):
        if(a & (1<<i)):
            ans+="1"
        else:
            ans+="0"
    return ans[::-1]

def computeMultiplicativeInverse(aux,a,mod):
    for i in range(253):
        a = mul(aux,a,mod)
    return a

def getMultiplicativeInverse(a):
    a = int("0x"+a,0)
    mod = int(pow(2,8)+pow(2,4)+pow(2,3)+pow(2,1)+pow(2,0))
    res = computeMultiplicativeInverse(a,a,mod)
    return hex(res).split('x')[1]

def getSboxValue(b,c):
	res = ""
	for i in range(8):
		res += str(int(b[i]) ^ int(b[(i+4)%8]) ^ int(b[(i+5)%8]) ^ int(b[(i+6)%8]) ^ int(b[(i+7)%8]) ^ int(c[i]))
	return res


def main():
	opc = int(input("1.- Multiplication in a binary field\n2.- Get the polynomial representation \n3.- Get the S-box value \nInput:"))
	if(opc == 1):
		print("All the values should be introduced using a binary representation")
		mod = input("Introduce the irreducible polynomial:")
		mod = int(getNumber(mod))
		a = input("Introduce number A:")
		a = int(getNumber(a))
		b = input("Introduce number B:")
		b = int(getNumber(b))
		ans = mul(a,b,mod)
		ans = getString(ans)
		print("Answer: " + str(ans))
	elif(opc == 2):
		print("All the values should be introduced using a binary representation")
		a = input("Introduce number A:")
		ans = getPoly(a)
		print("Answer: "+str(ans))
	else:
		print("All the values should be introduced using HEXADECIMAL values")
		a = input("Introduce number A: ")
		b = getMultiplicativeInverse(a)
		print("Its multiplicative inverse is "+str(b))
		b = int("0x"+b,0) #Ya es entero
		b = getString(b)# Sacamos la cadena binaria
		b = b[::-1]# Volteamos esa cadena
		# Llenamos de ceros si hacen falta
		while(len(b) < 8):
			b+='0'
		c = "11000110"# Definida por default
		ans = getSboxValue(b,c)
		ans = ans[::-1]# Volteamos lo obtenido
		ans = getNumber(ans)# Obtenemos el entero de la cadena binaria
		ans = hex(ans)# Obtenemos el hexa del entero
		print("Answer: " + str(ans))
    
main()
