import expanding

def findCoefficients(strFactor):
  strFactor = strFactor.replace('-','+-').replace(' ',"").replace("++","+")

  if strFactor[0]=="+":
    strFactor = strFactor[1:]

  coeffs = {}

  terms = strFactor.split("+")
  for t in range(len(terms)):
    if len(terms[t])>=1 and terms[t][0] =="x":
      terms[t] = "1"+terms[t]
    elif len(terms[t])>=2 and terms[t][0:2] =="-x":
      terms[t] = "-1"+terms[t][1:]
    if len(terms[t])>=1 and terms[t][-1]=="x":
      terms[t]+="^1"
    elif len(terms[t])>=1 and "x" not in terms[t]:
      terms[t]+="x^0"
    if "x^" in terms[t]:
      coeff, exp = terms[t].split("x^")
      if int(exp) in coeffs:
        coeffs[int(exp)] += float(coeff)
      else:
        coeffs[int(exp)] = float(coeff)
  return coeffs

def findMax(dict):
  m = 0
  for x in dict:
    if x>m:
      m=x
  return m

def syntheticDiv(coefficients, roots):
  coeffs = coefficients
  for root in roots:
    newCoeffs={}
    maxExp = findMax(coeffs)
    newCoeffs[maxExp-1] = coeffs[maxExp]
    for i in range(maxExp-1, 0, -1):
      if i not in coeffs:
        coeffs[i]=0
      newCoeffs[i-1] = newCoeffs[i]*root+coeffs[i]
    coeffs = newCoeffs
  for c in coeffs:
    coeffs[c] = round(coeffs[c],2)
  return coeffs 



def findDerivative(coeffs):
  deriv={}
  for exp in coeffs:
    if exp>0:
      deriv[exp-1] = coeffs[exp]*exp
  return deriv

def plugIn(x, coeffs):
  summ = 0
  for exp in coeffs:
    summ+=coeffs[exp]*(x**exp)
  return summ

def closeTo(x,a):
  return abs(x-a)<0.000000001

def newtonMethod(strFactor):
    letter = "x"
    for char in strFactor:
      if char.isalpha() and char!="x":
          letter = char
          strFactor=strFactor.replace(char, "x")
          break
      elif char=="x":
          break

    toFind, desmosUseless = expanding.wrapper(strFactor)
    coeffs = findCoefficients(toFind)
    deriv = findDerivative(coeffs)

    maxExp = 0
    for exp in coeffs:
      if exp>maxExp:
        maxExp = exp

    rootsNoRepeat = []
    roots = []

    for x0 in range(0,101):
        
      if len(roots)==maxExp:
        break
      y = plugIn(x0,coeffs)
      xn = x0
      count = 0
      while not closeTo(y,0) and count<100:
        d = plugIn(xn, deriv)
        if not closeTo(d,0):
          xn = xn-y/(d)
        else:
          break
        y = plugIn(xn,coeffs)
        count+=1
      
      xn = round(float(xn),2)
      if xn==int(xn):
        xn = int(xn)

      if closeTo(y,0) and xn not in roots:
        roots.append(xn)
        rootsNoRepeat.append(xn)
        nextDeriv = deriv
        d = plugIn(xn,deriv)
        while closeTo(d,0) and len(nextDeriv)>0:
          roots.append(xn)
          nextDeriv = findDerivative(nextDeriv)
          d = plugIn(xn, nextDeriv)
      
      
      if len(roots)==maxExp:
        break
      if x0!=0:
        y = plugIn(-x0,coeffs)
        xn = -x0
        count = 0
        while not closeTo(y,0) and count<100:
          d = plugIn(xn, deriv)
          if not closeTo(d,0):
            xn = xn-y/(d)
          else:
            break
          y = plugIn(xn,coeffs)
          count+=1

        xn = round(float(xn),2)
        if xn==int(xn):
          xn = int(xn)

        if closeTo(y,0) and xn not in roots:
          roots.append(xn)
          rootsNoRepeat.append(xn)
          nextDeriv = deriv
          d = plugIn(xn,deriv)
          while closeTo(d,0):
            roots.append(xn)
            nextDeriv = findDerivative(deriv)
            d = plugIn(xn,nextDeriv)
        
    multiplicities = {}
    for root in roots:
      if root in multiplicities:
        multiplicities[root]+=1
      else:
        multiplicities[root]=1

    synCoeffs = syntheticDiv(coeffs,roots)

    strFinal = ""
    #a = coeffs[maxExp]
    #if a==-1:
      #strFinal = "-"
    #elif a==1:
      #strFinal = ""
    #else:
      #strFinal = str(a)
    for root in multiplicities:
      if root==0:
        strFinal+="x"
      else:
        strFinal+="(x-"+str(root)+")"
      if multiplicities[root]>1:
        strFinal+="^"+str(multiplicities[root])+" "

    strFinal+="("
    for x in range(maxExp,-1,-1):
      if x in synCoeffs and synCoeffs[x]!=0:
        if synCoeffs[x]==1:
          strFinal+="+x^"+str(x)
        elif synCoeffs[x]==-1:
          strFinal+="-x^"+str(x)
        else:
          strFinal+="+"+str(synCoeffs[x])+"x^"+str(x)

    if strFinal[-1]=="(":
      strFinal = strFinal[:-1]
    else:
      strFinal = strFinal.replace("x^1","x").replace("+x^0","+1").replace("-x^0","-1").replace("x^0","").replace("+-","-").replace("(+","(")
      strFinal+=")"
      strFinal = strFinal.replace("(1)","")


    desmosForm = strFinal.replace("--","+")
    strFinal = desmosForm.replace("x",letter)
    return strFinal

def multiply(coeffs, nomialsArr, i=1):
    if i==len(nomialsArr):
        return coeffs
    else:
        newCoeffs = {}
        coeffs2 = findCoefficients(nomialsArr[i])
        for exp1 in coeffs:
            for exp2 in coeffs2:
                if exp1+exp2 in newCoeffs:
                    newCoeffs[exp1+exp2] += coeffs[exp1]*coeffs2[exp2]
                else:
                    newCoeffs[exp1+exp2] = coeffs[exp1]*coeffs2[exp2]
        return multiply(newCoeffs,nomialsArr,i+1)

def expandPoly(strToExpand):
    if strToExpand[0]!= "(":
        index = strToExpand.find("(")
        strToExpand = "("+strToExpand[:index]+")"+  strToExpand[index:]
    if strToExpand[-1]!= ")":
        index = strToExpand.rfind(")")
        strToExpand = strToExpand[:index+1]+"("+  strToExpand[index+1:]+")"
    print(strToExpand)
    strToExpand = strToExpand.replace(" ","").replace("*","")
    nomials = strToExpand.split("(")
    nomials.pop(0)
    for n in range(len(nomials)):
        if ")^" in nomials[n]:
            term, exp = nomials[n].split(")^")
            nomials[n] = term
            for x in range(int(exp)-1):
                nomials.append(term)
        else:
            nomials[n] = nomials[n][:-1]
    firstTerm = findCoefficients(nomials[0])
    expandedCoeff = multiply(firstTerm, nomials)
    maxExp = max(expandedCoeff.keys())
    expanded=""
    for ex in range(maxExp,-1,-1):
        if ex in expandedCoeff and round(expandedCoeff[ex],2)!=0:
            expandedCoeff[ex] = round(expandedCoeff[ex],2)
            if expandedCoeff[ex]==1:
              expanded+="+x^"+str(ex)
            elif expandedCoeff[ex]==-1:
              expanded+="+-x^"+str(ex)
            else:
              expanded+="+"+str(expandedCoeff[ex])+"x^"+str(ex)
    expanded = expanded[1:].replace("x^1","x").replace("+x^0","+1").replace("-x^0","-1").replace("x^0","").replace("+-","-")
    return expanded


