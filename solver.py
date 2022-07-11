import re
import copy
from simpleeval import simple_eval
from itertools import product

final = ['' for i in range(8)]
history = []
possible = ['0','1','2','3','4','5','6','7','8','9','+','-','*','/','=']
tried = [set() for i in range(8)]
must = []


doubleOperator = ["++", "--", "**", "//", "==", "+-", "+*", "+/", "+=", "-+","-*", "-/","-=", "*+", "*-","*/","*=", "/+", "/-", "/*","/=", "=+", "=-", "=*", "=/"]
basicOperator = ['+','-','*','/']

text = "7*9-3=60"
        
def checkMathFromString(sentence):
    try:
        sentence = sentence.split()[0]
        if len(sentence)!=8:
            return False
        
        if len(re.findall(r"([0-9]|[+]|[-]|[*]|[/]|[=]+)", sentence))!=len(sentence):
            return False
        
        if sentence[0]=='+' or sentence[0]=='-' or sentence[0]=='*' or sentence[0]=='/' or sentence[0]=='=':
            return False

        for dop in doubleOperator:
            if dop in sentence:
                return False
        
        idx = sentence.index('=')
        for bop in basicOperator:
            if bop in sentence[idx:]:
                return False

        sentence = sentence[:idx] + '=' +sentence[idx:]
        # return eval(sentence)
        return simple_eval(sentence)
    except:
        return False

def storeResult(sentence, result):
    history.append(sentence)

    sentence = sentence.replace(' ', '')
    result = result.replace(' ', '')
    for i in range(len(result)):
        if result[i]=='0':
            indices = []
            for j in range(len(sentence)):
                if sentence[j]==sentence[i]:
                    indices.append(j)
            deleted = True
            for idx in indices:
                if result[idx]!='0':
                    deleted = False
            if sentence[i] in possible and deleted:
                possible.remove(sentence[i])
        elif result[i]=='1':
            must.append(sentence[i])
        elif result[i]=='2':
            final[i] = sentence[i]
            if sentence[i] in must:
                must.remove(sentence[i])
        tried[i].add(sentence[i])

def notFinal():
    total = 0
    for i in range(8):
        if final[i]=='':
            total+=1
    return total

def uniqueCount(arr):
    opr = set()
    opd = set()
    for i in range(len(arr)):
        if arr[i]=='+' or arr[i]=='-' or arr[i]=='*' or arr[i]=='/' or arr[i]=='=':
            opr.add(arr[i])
        else:
            opd.add(arr[i])
    return len(opr),len(opd)
        
def generate():
    needed = notFinal()
    if len(possible)>8:
        return "12/4+5=8"
    comb = product(possible, repeat=needed)
    best = ""
    opr = 0
    opd = 0

    for kombinasi in comb:
        tempFinal = copy.copy(final)
        idx = 0
        cont = True
        for i in range(needed):
            while(tempFinal[idx]!=''):
                idx+=1
            if kombinasi[i] in tried[idx]:
                cont = False
            tempFinal[idx] = kombinasi[i]
            idx+=1
        if cont:
            kombString = ''.join(tempFinal)
            if kombString not in history:
                for i in range(len(must)):
                    if must[i] not in kombString:
                        cont=False
                if checkMathFromString(kombString) and cont:
                    # print(kombString)
                    tempOpr, tempOpd = uniqueCount(kombString)
                    if tempOpd>opd or (tempOpd==opd and tempOpr>opr):
                        best = kombString
                        opr = tempOpr
                        opd = tempOpd
    return best

            

# 0 untuk gagal, 1 salah tempat, 2 benar

###########################################################


while notFinal()>0:
    print("Rekomendasi:", text)
    res = input("Masukkan hasil: ")
    storeResult(text, res)

    text = generate()