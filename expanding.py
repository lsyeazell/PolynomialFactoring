

def findCoefficients(strFactor):
  if strFactor[0]=="+":
    strFactor = strFactor[1:]
  coeffs = {}
  terms = strFactor.split("+")

  for t in range(len(terms)):
    if len(terms[t])>=1 and terms[t][0] =="x":
      terms[t] = "1"+terms[t]
    elif len(terms[t])>=2 and terms[t][0:2] =="-x":
      terms[t] = "-1"+terms[t][1:]
    if len(terms[t])>=1 and "x" not in terms[t]:
      terms[t]+="x^0"
    elif len(terms[t])>=1 and "x" in terms[t] and "^" not in terms[t]:
      loc = terms[t].find("x")
      terms[t] = terms[t][:loc+1]+"^1"+terms[t][loc+1:]
    if "x^" in terms[t]:
      coeff2=None
      star=terms[t].rfind("*")
      if "*" in terms[t] and star> terms[t].find("^"):
          coeff2 = float(terms[t][star+1:])
          terms[t] = terms[t][:star]
      coeff, exp = terms[t].split("x^")
      if coeff[-1]=="*":
          coeff = coeff[:-1]
      coeff = eval(coeff)
      if coeff2:
          coeff = coeff*coeff2
      if int(exp) in coeffs:
        coeffs[int(exp)] += coeff
      else:
        coeffs[int(exp)] = coeff

  return coeffs

def addCoeffs(coeffs1, coeffs2):
    newCoeffs = {}
    for c1 in coeffs1:
        if c1 in coeffs2:
            newCoeffs[c1] = coeffs1[c1]+coeffs2[c1]
        else:
            newCoeffs[c1] = coeffs1[c1]
    for c2 in coeffs2:
        if not c2 in coeffs1:
            newCoeffs[c2] = coeffs2[c2]
    return newCoeffs

def multiCoeffs(coeffs1, coeffs2):
    newCoeffs = {}
    for exp1 in coeffs1:
        for exp2 in coeffs2:
            if exp1+exp2 in newCoeffs:
                newCoeffs[exp1+exp2] += coeffs1[exp1]*coeffs2[exp2]
            else:
                newCoeffs[exp1+exp2] = coeffs1[exp1]*coeffs2[exp2]
    return newCoeffs

def splitByPlus(expr):
    if expr[0]=="+":
        expr=expr[1:]
    balance = 0
    subExpr = []
    iPrev = 0
    for i in range(len(expr)):
        char = expr[i]
        if char =="+" and balance == 0:
            subExpr.append(expr[iPrev:i])
            iPrev=i+1
        elif char=="(":
            balance+=1
        elif char==")":
            balance-=1
    subExpr.append(expr[iPrev:])
    return subExpr

def simplify2(expression):
    if expression=="":
        return {}
    if "(" not in expression:
        return findCoefficients(expression)
    else:
        subExpr = splitByPlus(expression)
        simpExpr = []
        for expr in subExpr:
            
            if not "(" in expr:
                simpExpr.append(findCoefficients(expr))
                continue
            #Parentheses
            ind = expr.find("(")
            ind2 = ind
            balance = 1
            while balance !=0:
                ind2+=1
                if expr[ind2]==")":
                    balance-=1
                elif expr[ind2]=="(":
                    balance+=1
            myCoeffs = simplify2(expr[ind+1:ind2])
            if ind==0 and ind2==len(expr)-1:
                simpExpr.append(myCoeffs)
                continue
            
            #Exponents
            if ind2!=len(expr)-1 and expr[ind2+1:ind2+3]=="**":
                ind3 = ind2+3    
                while ind3<len(expr) and expr[ind3].isdigit():
                    ind3+=1
                newCoeffs = myCoeffs
                for i in range(int(expr[ind2+3:ind3])-1):
                    newCoeffs = multiCoeffs(newCoeffs, myCoeffs)
                myCoeffs =newCoeffs
                ind2 = ind3-1

            #multiply
            if ind!=0 and expr[ind-1]=="-":
                expr = expr[:ind]+"1*"+expr[ind:]
                ind+=2
                ind2+=2
            if ind!=0 and (expr[ind-1].isdigit() or expr[ind-1]=="x"):
                expr = expr[:ind]+"*"+expr[ind:]
                ind+=1
                ind2+=1

            if ind2!=len(expr)-1 and expr[ind2+1]=="*":
                myCoeffs= multiCoeffs(myCoeffs,simplify2(expr[ind2+2:]))
            elif ind2!=len(expr)-1 and expr[ind2+1]=="(":
                myCoeffs= multiCoeffs(myCoeffs,simplify2(expr[ind2+1:]))

            if ind!=0 and expr[ind-1]=="*":
                myCoeffs=  multiCoeffs(myCoeffs,simplify2(expr[:ind-1]))
            elif ind!=0 and expr[ind-1]==")":
                myCoeffs=  multiCoeffs(myCoeffs,simplify2(expr[:ind]))

            simpExpr.append(myCoeffs)

        #add
        if len(simpExpr)==1:
            return simpExpr[0]
        elif len(simpExpr)==2:
            return addCoeffs(simpExpr[0],simpExpr[1])
        else:
            summ = addCoeffs(simpExpr[0],simpExpr[1])
            for i in range(len(simpExpr)-2):
                summ = addCoeffs(summ, simpExpr[i+2])
            return summ

def coeffToStr(coeffs):
    maxExp = max(coeffs.keys())
    string=""
    for exp in range(maxExp,-1,-1):
        
        if exp in coeffs and coeffs[exp]!=0:
            if int(coeffs[exp])==coeffs[exp]:
                coeffs[exp]=int(coeffs[exp])
            if coeffs[exp]==1:
              string+="+x^"+str(exp)
            elif coeffs[exp]==-1:
              string+="+-x^"+str(exp)
            else:
              string+="+"+str(coeffs[exp])+"x^"+str(exp)
    string = string[1:].replace("x^1","x").replace("+x^0","+1").replace("-x^0","-1").replace("x^0","").replace("+-","-")
    return string

def wrapper(expr):
    letter = "x"
    for char in expr:
        if char.isalpha() and char!="x":
            letter = char
            expr=expr.replace(char, "x")
            break
        elif char=="x":
            break
    expr = expr.replace("--","-").replace('-','+-').replace(' ',"").replace("++","+").replace("*+","*").replace("(+","(").replace(")x", ")*x")
    while "^(" in expr:
        ind = expr.rfind("^(")
        ind2 = expr[ind:].find(")")+ind
        expr = expr[:ind]+"**"+str(eval(expr[ind+2:ind2]))+expr[ind2+1:]
    expr = expr.replace("^","**").replace("x**","x^")
    desmosForm = coeffToStr(simplify2(expr))
    finalStr = desmosForm.replace("x",letter)
    return finalStr, desmosForm

        
