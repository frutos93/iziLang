import sys
import scanner as scanner
import turtle


currentPointer = 1
memoriesStack = []
pointersStack = []
tipoFuncion = []
funcionesDir = {}
constantes = {}
parametrosEnMemoria = {101: 8000, 102: 9000, 103: 10000, 104: 11000}
memoriaEjecucion  = [{},[{}],[{}],constantes]
cuadruplos = []
inner = 0

def cargaDatosEnMemoria():
    global funcionesDir
    parametrosFuncion = []
    era = [0,0,0,0]
    for funcion in scanner.dirFunciones:
        
        if (not(funcion == 'constantes' or funcion == 'global' or funcion == 'MAIN')):
            nombre = funcion
            for parametro in scanner.dirFunciones[funcion]["parametros"]:
                parametrosFuncion.append(parametro)
            regreso = scanner.dirFunciones[funcion]['return'] #no se llama return porque es palabra reservada
            memoria = scanner.dirFunciones[funcion]['memoria']
            cuadruploID = scanner.dirFunciones[funcion]['cuadruploIndice']
            for variables in scanner.dirFunciones[funcion]['variables']:
                era[scanner.dirFunciones[funcion]['variables'][variables]['tipo'] - 101] += 1
            era[0] += scanner.dirFunciones[funcion]['temporales'][101]
            era[1] += scanner.dirFunciones[funcion]['temporales'][102]
            era[2] += scanner.dirFunciones[funcion]['temporales'][103]
            era[3] += scanner.dirFunciones[funcion]['temporales'][104]
            funcionesDir[funcion] = {'parametros': parametrosFuncion, 'return': regreso, 'memoria':memoria, 'cuadruplo':cuadruploID, 'era':era}


    for constante in scanner.dirFunciones["constantes"]:
        tipo = scanner.dirFunciones['constantes'][constante]['tipo']
        memoria = scanner.dirFunciones['constantes'][constante]['memoria']
        valor = constante
        if(tipo == 101):
            constantes[memoria] = {'tipo': tipo, 'valor': valor}
        elif(tipo == 102):
            constantes[memoria] = {'tipo': tipo, 'valor': valor}
        else:
            constantes[memoria] = {'tipo': tipo, 'valor': valor}
    for cuadruplo in scanner.cuadruplos:
        oper = cuadruplo[0]
        oper1 = cuadruplo[1]
        oper2 = cuadruplo[2]
        result = cuadruplo[3]
        cuadruplos.append([oper,oper1,oper2,result])





def getMemoryValue(memoria):
    global memoriaEjecucion, inner
    if(memoria < 8000):
        return memoriaEjecucion[0][memoria]
    elif (memoria < 14000):
        return memoriaEjecucion[1][-1-inner][memoria]
    elif (memoria < 20000):
        return memoriaEjecucion[2][-1-inner][memoria]
    else:
        return memoriaEjecucion[3][memoria]['valor']

def saveValueMemory(result, memoria):
    global memoriaEjecucion, inner
    if (memoria < 8000):
        memoriaEjecucion[0][memoria] = result
    elif (memoria < 14000):
        memoriaEjecucion[1][-1 - inner][memoria] = result
    elif (memoria < 20000):
        memoriaEjecucion[2][-1 - inner][memoria] = result
    else:
        memoriaEjecucion[3][-1 - inner][memoria] = result




def operacion(cuadruplo):
    oper1 = cuadruplo[1]
    oper1 = getMemoryValue(oper1)
    oper2 = cuadruplo[2]
    oper2 = getMemoryValue(oper2)

    if(cuadruplo[0] == 0):
        saveValueMemory(int(oper1)+int(oper2),cuadruplo[3])
    elif(cuadruplo[0] == 1):
        saveValueMemory(int(oper1) * int(oper2), cuadruplo[3])
    elif(cuadruplo[0] == 2):
        saveValueMemory(int(oper1) - int(oper2), cuadruplo[3])
    elif (cuadruplo[0] == 3):
        saveValueMemory(int(oper1) / int(oper2), cuadruplo[3])
    elif (cuadruplo[0] == 4):
        saveValueMemory(int(oper1) & int(oper2), cuadruplo[3])
    elif (cuadruplo[0] == 5):
        saveValueMemory(int(oper1) | int(oper2), cuadruplo[3])
    elif (cuadruplo[0] == 6):
        saveValueMemory(int(oper1) < int(oper2), cuadruplo[3])
    elif (cuadruplo[0] == 7):
        saveValueMemory(int(oper1) > int(oper2), cuadruplo[3])
    elif (cuadruplo[0] == 8):
        saveValueMemory(int(oper1) != int(oper2), cuadruplo[3])
    elif (cuadruplo[0] == 9):
        saveValueMemory(int(oper1) == int(oper2), cuadruplo[3])
    elif (cuadruplo[0] == 10):
        saveValueMemory(int(oper1) <= int(oper2), cuadruplo[3])
    elif (cuadruplo[0] == 11):
        saveValueMemory(int(oper1) >= int(oper2), cuadruplo[3])

def setMemoryParameter(memoria, result):
    global memoriaEjecucion
    result = getMemoryValue(result)
    if (memoria < 8000):
        memoriaEjecucion[0][-1][memoria] = result
    elif (memoria < 14000):
        memoriaEjecucion[1][-1][memoria] = result
    elif (memoria < 20000):
        memoriaEjecucion[2][-1][memoria] = result
    else:
        memoriaEjecucion[3][-1][memoria] = result

def getMemoryParam(param):
    global parametrosEnMemoria
    temp = parametrosEnMemoria[param]
    parametrosEnMemoria[param] += 1
    return temp


def reiniciaEra():
    global memoriaEjecucion
    memoriaEjecucion[1].pop()
    memoriaEjecucion[2].pop()

def iniciaEra():
    global memoriaEjecucion
    memoriaEjecucion[1].append({})
    memoriaEjecucion[2].append({})
def memoriaParametros():
    global parametrosEnMemoria
    parametrosEnMemoria = {101: 8000, 102: 9000, 103: 10000, 104: 11000}

def run():
    global currentPointer, memoriaEjecucion, constantes, inner, funcionesDir
    scanner.parse()
    scanner.cuadruplos.append(['FIN', -1, -1, -1])
    cargaDatosEnMemoria()
    memoriaEjecucion[3] = constantes
    cuadruploActual = cuadruplos[currentPointer-1]
    currentPointer += 1
    while cuadruploActual[0] != 'FIN':
        instruccion = cuadruploActual[0]
        if(instruccion < 12):
            operacion(cuadruploActual)
        elif(instruccion == 12):
            saveValueMemory(getMemoryValue(cuadruploActual[1]),cuadruploActual[3])
        elif(instruccion == 13):
            currentPointer = cuadruploActual[3] -1
        elif(instruccion == 14):
            if(getMemoryValue(cuadruploActual[1]) == False):
                currentPointer = cuadruploActual[3] - 1
        elif(instruccion == 15):
            print "PRINT: ", getMemoryValue(cuadruploActual[3])
        elif(instruccion == 19):
            turtle.fd(cuadruploActual[3])
        elif(instruccion == 20):
            reiniciaEra()
            currentPointer = memoriesStack.pop()
            tipoFuncion.pop()
            memoriaParametros()
        elif(instruccion == 21):
            iniciaEra()
            tipoFuncion.append(cuadruploActual[3])
            inner = 1
        elif(instruccion == 22):
            inner = 0
            memoriesStack.append(currentPointer)
            currentPointer = funcionesDir[cuadruploActual[3]]['cuadruplo'] -1
            memoriaParametros()
        elif(instruccion == 23):
            tipo = funcionesDir[tipoFuncion[-1]]['parametros'][cuadruploActual[3]-1]
            temp = getMemoryParam(tipo)
            setMemoryParameter(temp, cuadruploActual[1])
        elif(instruccion == 24):
            saveValueMemory(getMemoryValue(cuadruploActual[3]),funcionesDir[tipoFuncion[-1]]['memoria'])
            reiniciaEra()
            currentPointer = memoriesStack.pop()
            tipoFuncion.pop()
        cuadruploActual = cuadruplos[currentPointer]
        currentPointer += 1
    turtle.fd(1)
    turtle.done()



run()
