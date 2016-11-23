import sys
import scanner as scanner
import turtle


timeDebug = False
debug = False

funcionesDir = {}
spriteSet = {}
mapping = {}
map = {}
objectsCount = {}
movableObjects = []
spawnerObjects = []
mapRow = 0
mapCol = 0
maxMapRow = 0
maxMapCol = 0
score = 0
time = 0
tileWidth = 50
tileHeight = 50
constantes = {}
cuadruplos = []
currentPointer = 1
instructionStack = []
functionScope = []
parametersMemoryValues = {101: 8000,  102: 9000,  103: 10000, 104: 11000}
offset = 0
protectFrom = ""
protect = ""
protectTile = ()
spriteInTile = []
win = None
clock = None
avatarPos = (0, 0)
tile = (0, -1)

# Memory of execution
memoriaEjecucion = memoriaEjecucion = [{}, [{}], [{}], constantes]


def getSection(value):
    if (value < 8000):
        return 0
    elif (value < 14000):
        return 1
    elif (value < 20000):
        return 2
    else:
        return 3


def saveValueMemory(value, memoryKey):
    global memoriaEjecucion, offset
    if (memoryKey < 0):
        memoryKey = getMemoryValue(-1 * memoryKey)
    section = getSection(memoryKey)
    if (section == 0):
        memoriaEjecucion[section][memoryKey] = value
    else:
        memoriaEjecucion[section][-1 - offset][memoryKey] = value


def getMemoryValue(memoryKey):
    global memory, offset
    if (memoryKey < 0):
        memoryKey = getMemoryValue(-1 * memoryKey)
    section = getSection(memoryKey)
    if (debug):
        print "GET = accessing value in section: ", section
    if (section == 0):
        return memoriaEjecucion[section][memoryKey]
    elif (section == 3):
        return memoriaEjecucion[section][memoryKey]['valor']
    else:
        return memoriaEjecucion[section][-1 - offset][memoryKey]


def createERAInMemory():
    global memoriaEjecucion
    memoriaEjecucion[1].append({})
    memoriaEjecucion[2].append({})


def deleteERAInMemory():
    global memoriaEjecucion
    memoriaEjecucion[1].pop()
    memoriaEjecucion[2].pop()


def assignParamInMemory(memoryKey1, memoryKey2):
    global memoriaEjecucion, offset
    if (memoryKey2 < 0):
        memoryKey2 = getMemoryValue(-1 * memoryKey2)
    section = getSection(memoryKey2)
    value = getMemoryValue(memoryKey1)
    if (debug):
        print "Assigning parameters: ", memoryKey1, memoryKey2, value
        memoriaEjecucion[section][-1][memoryKey2] = value


def getParamMemoryValue(paramType):
    global parametersMemoryValues
    value = parametersMemoryValues[paramType]
    parametersMemoryValues[paramType] += 1
    return value


def resetParametersMemoryValues():
    global parametersMemoryValues
    parametersMemoryValues = {101: 8000,  102: 9000,  103: 10000, 104: 11000}


def cargaDatosAMemoria():
    global funcionesDir, cuadruplos,constantes
    parametrosFuncion = []
    era = [0, 0, 0, 0]
    for funcion in scanner.dirFunciones:
        if (not (funcion == 'constantes' or funcion == 'global' or funcion == 'MAIN')):
            for parametro in scanner.dirFunciones[funcion]["parametros"]:
                parametrosFuncion.append(parametro)
            regreso = scanner.dirFunciones[funcion]['return']  # no se llama return porque es palabra reservada
            memoria = scanner.dirFunciones[funcion]['memoria']
            cuadruploID = scanner.dirFunciones[funcion]['cuadruploIndice']
            for variables in scanner.dirFunciones[funcion]['variables']:
                era[scanner.dirFunciones[funcion]['variables'][variables]['tipo'] - 101] += 1
            era[0] += scanner.dirFunciones[funcion]['temporales'][101]
            era[1] += scanner.dirFunciones[funcion]['temporales'][102]
            era[2] += scanner.dirFunciones[funcion]['temporales'][103]
            era[3] += scanner.dirFunciones[funcion]['temporales'][104]
            funcionesDir[funcion] = {'parametros': parametrosFuncion, 'return': regreso, 'memoria': memoria,
                                     'cuadruplo': cuadruploID, 'era': era}

    for constante in scanner.dirFunciones["constantes"]:
        tipo = scanner.dirFunciones['constantes'][constante]['tipo']
        memoria = scanner.dirFunciones['constantes'][constante]['memoria']
        valor = constante
        if (tipo == 101):
            constantes[memoria] = {'tipo': tipo, 'valor': valor}
        elif (tipo == 102):
            constantes[memoria] = {'tipo': tipo, 'valor': valor}
        else:
            constantes[memoria] = {'tipo': tipo, 'valor': valor}
    for cuadruplo in scanner.cuadruplos:
        oper = cuadruplo[0]
        oper1 = cuadruplo[1]
        oper2 = cuadruplo[2]
        result = cuadruplo[3]
        cuadruplos.append([oper, oper1, oper2, result])

def math(cuadruplo):
    oper1 = cuadruplo[1]
    oper1 = getMemoryValue(oper1)
    oper2 = cuadruplo[2]
    oper2 = getMemoryValue(oper2)

    if (cuadruplo[0] == 0):
        saveValueMemory(int(oper1) + int(oper2), cuadruplo[3])
    elif (cuadruplo[0] == 1):
        saveValueMemory(int(oper1) * int(oper2), cuadruplo[3])
    elif (cuadruplo[0] == 2):
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
    
def acciones(cuadruplo):
    global currentPointer, funcionesDir, instructionStack, functionScope, offset, spriteSet, map, score, mapRow, mapCol, mapping, objectsCount, time, maxMapRow, maxMapCol, tileWidth, tileHeight, win, clock, avatarPos, tile, movableObjects, protect, spriteInTile, protectFrom, protectTile, spawnerObjects
    if (cuadruplo[0] <= 11):
        math(cuadruplo)
        return True
    elif (cuadruplo[0] == 12):
        result = getMemoryValue(cuadruplo[1])
        saveValueMemory(result, cuadruplo[3])
        return True
    elif (cuadruplo[0] == 13):
        currentPointer = cuadruplo[3] - 1
        return True
    elif (cuadruplo[0] == 14):
        result = getMemoryValue(cuadruplo[1])
        if (debug):
            print "GOTOF result: ", result
        if (result == False):
            currentPointer = cuadruplo[3] - 1
        return True
    elif (cuadruplo[0] == 15):
        result = getMemoryValue(cuadruplo[3])
        print "PRINT: ", result
        return True
    elif (cuadruplo[0] == 16):
        return True
    elif (cuadruplo[0] == 17):
        return True
    elif (cuadruplo[0] == 18):
        return True
    elif (cuadruplo[0] == 19):
        turtle.fd(cuadruplo[3])
        return True
    elif (cuadruplo[0] == 20):
        deleteERAInMemory()
        currentPointer = instructionStack.pop()
        functionScope.pop()
        resetParametersMemoryValues()
        return True
    elif (cuadruplo[0] == 21):
        createERAInMemory()
        functionScope.append(cuadruplo[3])
        offset = 1
        return True
    elif (cuadruplo[0] == 22):
        function = cuadruplo[3]
        instructionStack.append(currentPointer)
        offset = 0
        currentPointer = funcionesDir[function]['cuadruplo'] - 1
        resetParametersMemoryValues()
        return True
    elif (cuadruplo[0] == 23):
        value = cuadruplo[1]
        paramType = funcionesDir[functionScope[-1]]['parametros'][cuadruplo[3] - 1]
        param = getParamMemoryValue(paramType)
        assignParamInMemory(value, param)
        return True
    elif (cuadruplo[0] == 24):
        result = getMemoryValue(cuadruplo[3])
        saveValueMemory(funcionesDir[functionScope[-1]]['memoria'], result)
        deleteERAInMemory()
        currentPointer = instructionStack.pop()
        functionScope.pop()
        return True
    elif (cuadruplo[0] == 25):
        result = getMemoryValue(cuadruplo[1])
        if (result >= cuadruplo[2] and result <= cuadruplo[3]):
            return True
        else:
            return False
    elif(cuadruplos[0] == 'FIN'):
        return False


argv = sys.argv[1:]
scanner.parse()
memoriaEjecucion[3] = constantes

cargaDatosAMemoria()
cuadruplos.append(['FIN',-1,-1,-1])
while 1:
    if (acciones(cuadruplos[currentPointer - 1])):
        currentPointer += 1;
    else:
        break;

print cuadruplos
turtle.done()