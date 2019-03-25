def basica(b,m):
    tam = log2(b)+1
    b = (b<<1);
    if(b&(1 << tam)):
        b = b^(m^(1<<tam))
    return b
    
def normal(a,b,m):
    tam = log2(a)+1
    i = 0
    res = 0
    while (i < tam):
        if(a &(1<<i)):
            aux = b
            for j in range(i):
                aux = basica(aux,m)
            res = res ^ aux
            i= i+1
    return res

def representation(s):
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

def main():
    print(representation("1100110"))
    
main()
    