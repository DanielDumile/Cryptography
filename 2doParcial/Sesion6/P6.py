import math

def basic(b,m):
    ult = int(math.log2(m))
    print("El ultimo es "+str(ult))
    flag = False
    b = b << 1
    print(getString(b))
    if (b&(1<<ult)):
        print("Esta prendido el ultimo")
        b = b ^ (1<<ult)
        print(getString(b))
        print("Despues del XOR nos da "+ str(b))
        b = b^(m^(1<<ult))
    return b
    
def mul(a,b,m):
    tam = int(math.log2(a))+1
    i = 0
    res = 0
    while (i < tam):
        if(a &(1<<i)):
            aux = b
            for j in range(i):
                aux = basic(aux,m)
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


def main():

    while True:
        a = input("Enter number A: ")
        a = int("0x"+a,0)
        print(a)
        print(getString(a))
        b = input("Enter number B: ")
        b = int("0x"+b,0)
        print(b)
        print(getString(b))
        #print(getPoly(a))
        #a = int(getNumber(a))
        #print(getPoly(b))
        #b = int(getNumber(b))
        #print(getPoly(mod))
        mod = int(getNumber("100011011"))
        mod = int(pow(2,8)+pow(2,4)+pow(2,3)+pow(2,1)+pow(2,0))
        #print(basic(b,mod))
        print("Resultado:")
        res = mul(a,b,mod)
        print(hex(res))
        #print(getPoly(getString(mul(a,b,mod))))
    
main()