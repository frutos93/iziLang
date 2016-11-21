import sys
import scanner as scanner



currentPointer = 0
memoriesStack = []
pointersStack = []
funcionesDir = {}
constantes = {}
memoriaEjecucion  = {{},{},{},constantes}
cuadruplos = []
inner = 0

def cargaDatosEnMemoria():
    global funcionesDir
    parametrosFuncion = []
    era = [0,0,0,0]
    for funcion in scanner.dirFunciones:
        if (funcion != 'contantes' & funcion != 'global' & funcion != 'main'):
            nombre = funcion
            for parametros in scanner.dirFunciones[funcion]['parametros']:
                parametrosFuncion.append(parametros)
            regreso = scanner.dirFunciones[funcion]['return'] #no se llama return porque es palabra reservada
            memoria = scanner.dirFunciones[funcion]['memoria']
            cuadruploID = scanner.dirFunciones[funcion]['start_cuadruplet']
            for variables in scanner.dirFunciones[funcion]['variables']:
                era[scanner.dirFunciones[funcion]['variables'][variables]['tipo'] - 101] += 1
            era[0] += scanner.dirFunciones[funcion]['temporals'][101]
            era[1] += scanner.dirFunciones[funcion]['temporals'][102]
            era[2] += scanner.dirFunciones[funcion]['temporals'][103]
            era[3] += scanner.dirFunciones[funcion]['temporals'][105]
            funcionesDir[funcion] = {'parametros': parametrosFuncion, 'return': regreso, 'memoria':memoria, 'cuadruplo':cuadruploID, 'era':era}.

    for constante in scanner.dirFunciones["constantes"]:
        tipo = scanner.dirFunciones[constante]['tipo']
        memoria = scanner.dirFunciones[constante]['memoria']
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
    if(memoria < 7000):
        return memoriaEjecucion[0][memoria]
    elif (memoria < 12000):
        return memoriaEjecucion[1][-1-inner][memoria]
    elif (memoria < 17000):
        return memoriaEjecucion[2][-1-inner][memoria]
    else:
        return memoriaEjecucion[3][memoria]['valor']

def saveValueMemory(result, memoria):
    global memoriaEjecucion, inner
    if (memoria < 7000):
        memoriaEjecucion[0][memoria] = result
    elif (memoria < 12000):
        memoriaEjecucion[1][-1 - inner][memoria] = result
    elif (memoria < 17000):
        memoriaEjecucion[2][-1 - inner][memoria] = result
    else:
        memoriaEjecucion[3][-1 - inner][memoria] = result




def operacion(cuadruplo):
    oper1 = cuadruplo[1]
    oper1 = getMemoryValue(oper1)
    oper2 = cuadruplo[2]
    oper2 = getMemoryValue(oper2)

    if(cuadruplo[0] == 0):
        saveValueMemory(oper1+oper2,cuadruplo[3])
    elif(cuadruplo[0] == 1):
        saveValueMemory(oper1 * oper2, cuadruplo[3])
    elif(cuadruplo[0] == 2):
        saveValueMemory(oper1 - oper2, cuadruplo[3])
    elif (cuadruplo[0] == 3):
        saveValueMemory(oper1 / oper2, cuadruplo[3])
    elif (cuadruplo[0] == 4):
        saveValueMemory(oper1 & oper2, cuadruplo[3])
    elif (cuadruplo[0] == 5):
        saveValueMemory(oper1 | oper2, cuadruplo[3])
    elif (cuadruplo[0] == 6):
        saveValueMemory(oper1 < oper2, cuadruplo[3])
    elif (cuadruplo[0] == 7):
        saveValueMemory(oper1 > oper2, cuadruplo[3])
    elif (cuadruplo[0] == 8):
        saveValueMemory(oper1 != oper2, cuadruplo[3])
    elif (cuadruplo[0] == 9):
        saveValueMemory(oper1 == oper2, cuadruplo[3])



def run(fileName):
    global currentPointer, memoriaEjecucion, constantes
    scanner.cuadruplos.append(['FIN', -1, -1, -1])
    cargaDatosEnMemoria()
    memoriaEjecucion[3] = constantes
    cuadruploActual = cuadruplos[currentPointer]
    currentPointer += 1
    while cuadruploActual[0] != 'FIN':
        if(cuadruploActual[0] < 10):
            operacion(cuadruploActual)
            cuadruploActual = cuadruplos[currentPointer]
            currentPointer += 1
        elif(cuadruploActual[0] == 10):
            saveValueMemory(getMemoryValue(cuadruploActual[1]),cuadruploActual[3])
        elif(cuadruploActual[0] == 11):



