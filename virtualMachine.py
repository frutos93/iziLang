# -*- coding: utf-8 -*-
import sys
import scanner as scanner
import turtle
import math


#variables globales de memoria, parametros y listas para control inicializadas.
currentPointer = 1
memoriesStack = []
pointersStack = []
tipoFuncion = []
funcionesDir = {}
constantes = {}
parametrosEnMemoria = {101: 5000,  102: 6000,  103: 7000, 104: 8000}
memoriaEjecucion  = [{},[{}],[{}],constantes]
cuadruplos = []
inner = 0

#Metodo que carga todos los datos de scanner en la memoria de ejecucion
#guarda las funciones en un diccionario de funciones en memoria virtual al igual
#que guarda constantes y cuadruplos
def cargaDatosEnMemoria():
    global funcionesDir
    parametrosFuncion = []
    era = [0,0,0,0]
    #se guardan funciones
    for funcion in scanner.dirFunciones:
        if (not(funcion == 'constantes' or funcion == 'global' or funcion == 'MAIN')):
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

    #se guardan constantes
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
    #se guardan cuadruplos
    for cuadruplo in scanner.cuadruplos:
        oper = cuadruplo[0]
        oper1 = cuadruplo[1]
        oper2 = cuadruplo[2]
        result = cuadruplo[3]
        cuadruplos.append([oper,oper1,oper2,result])




#Accesa cierto pedazo de memoria y regresa el valor asignado a esa memoria
def getMemoryValue(memoria):
    global memoriaEjecucion, inner
    if inner == 1:
        cont = -2
    else:
        cont = -1
    if (memoria < 0):
        memoria *= -1
        memoria = getMemoryValue(memoria)
    if(memoria < 5000):
        return memoriaEjecucion[0][memoria]
    elif (memoria < 9000):
        return memoriaEjecucion[1][cont][memoria]
    elif (memoria < 13000):
        return memoriaEjecucion[2][cont][memoria]
    else:
        return memoriaEjecucion[3][memoria]['valor']

#Guarda un valor a una memoria, generalmente es cuando se desea guardar una memoria dentro de ejecucion
def saveValueMemory(result, memoria):
    global memoriaEjecucion, inner
    if inner == 1:
        cont = -2
    else:
        cont = -1
    if (memoria < 0):
        memoria *= -1
        memoria = getMemoryValue(memoria)
    if (memoria < 5000):
        memoriaEjecucion[0][memoria] = result
    elif (memoria < 9000):
        memoriaEjecucion[1][cont][memoria] = result
    elif (memoria < 13000):
        memoriaEjecucion[2][cont][memoria] = result
    else:
        memoriaEjecucion[3][cont][memoria] = result



#Genera el resultado de una operación aritmética y lo guarda en la memoria
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

#Actualiza un pedazo de memoria con cierto valor
def setMemoryParameter(memoria, result):
    global memoriaEjecucion
    result = getMemoryValue(result)
    if (memoria < 5000):
        memoriaEjecucion[0][-1][memoria] = result
    elif (memoria < 9000):
        memoriaEjecucion[1][-1][memoria] = result
    elif (memoria < 13000):
        memoriaEjecucion[2][-1][memoria] = result
    else:
        memoriaEjecucion[3][-1][memoria] = result

#Obtiene la dirección de cierto parametro
def getMemoryParam(param):
    global parametrosEnMemoria
    temp = parametrosEnMemoria[param]
    parametrosEnMemoria[param] += 1
    return temp

#reinicia la memoria completamente, de una funcion, solo local y temporal
def reiniciaEra():
    global memoriaEjecucion
    memoriaEjecucion[1].pop()
    memoriaEjecucion[2].pop()
#Inicia la memoria para ser usada en una funcion
def iniciaEra():
    global memoriaEjecucion
    memoriaEjecucion[1].append({})
    memoriaEjecucion[2].append({})

#Reinicia la memoria de los parametros
def memoriaParametros():
    global parametrosEnMemoria
    parametrosEnMemoria = {101: 5000,  102: 6000,  103: 7000, 104: 8000}

#Funcion principal que llamada la carga  a memoria y contien el ciclo principal de valores.
def run():
    global currentPointer, memoriaEjecucion, constantes, inner, funcionesDir
    direccion = 90
    offsetDireccion = 0
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
            saveValueMemory(getMemoryValue(cuadruploActual[1]), cuadruploActual[3])
        elif(instruccion == 13):
            currentPointer = int(cuadruploActual[3]) -1
        elif(instruccion == 14):
            if(getMemoryValue(cuadruploActual[1]) == False):
                currentPointer = cuadruploActual[3] - 1
        elif(instruccion == 15):
            print "IMPRIME: ", getMemoryValue(cuadruploActual[3])
        elif(instruccion == 16):
            turtle.right(270)
            turtle.fd(int(getMemoryValue(cuadruploActual[3])))
        elif(instruccion == 17):
            turtle.right(90)
            turtle.fd(int(getMemoryValue(cuadruploActual[3])))
        elif(instruccion == 18):
            turtle.right(180)
            turtle.fd(int(getMemoryValue(cuadruploActual[3])))
        elif(instruccion == 19):
            turtle.right(0)
            turtle.fd(int(getMemoryValue(cuadruploActual[3])))
        elif(instruccion == 20):
            reiniciaEra()
            currentPointer = memoriesStack.pop()
            tipoFuncion.pop()
            memoriaParametros()
        elif(instruccion == 21):
            iniciaEra()
            inner = 1
            tipoFuncion.append(cuadruploActual[3])
        elif(instruccion == 22):
            memoriesStack.append(currentPointer)
            inner = 0
            currentPointer = funcionesDir[cuadruploActual[3]]['cuadruplo'] - 1
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
        elif(instruccion == 25):
            valor = getMemoryValue(cuadruploActual[1])
            if (not(int(valor) >= int(cuadruploActual[2]) and int(valor) <= int(cuadruploActual[3]))):
                print ("error")
                break;
        elif(instruccion == 26):
            value = int(getMemoryValue(cuadruploActual[3]))
            offset = int(int(getMemoryValue(cuadruploActual[3]))/2)
            direccion = turtle.heading()
            turtle.penup()
            turtle.fd(offset)
            turtle.pendown()
            turtle.right(90)
            turtle.fd(offset)
            turtle.right(90)
            turtle.fd(value)
            turtle.right(90)
            turtle.fd(value)
            turtle.right(90)
            turtle.fd(value)
            turtle.right(90)
            turtle.fd(offset)
            turtle.penup()
            turtle.setheading(direccion)
            turtle.back(offset)
            turtle.pendown()

        elif(instruccion == 27):
            offset = int(int(getMemoryValue(cuadruploActual[3])) / 2)
            direccion = turtle.heading()
            turtle.penup()
            turtle.right(90)
            turtle.fd(offset)
            turtle.left(90)
            turtle.pendown()
            turtle.circle(offset)
            turtle.penup()
            turtle.left(90)
            turtle.fd(offset)
            turtle.right(90)
            turtle.setheading(direccion)
            turtle.pendown()

        elif(instruccion == 28):
            value1 = int(getMemoryValue(cuadruploActual[2]))
            value2 = int(getMemoryValue(cuadruploActual[3]))
            offset1 = int(value1 / 2)
            offset2 = int(value2/2)
            direccion = turtle.heading()
            turtle.penup()
            turtle.fd(offset1)
            turtle.pendown()
            turtle.right(90)
            turtle.fd(offset2)
            turtle.right(90)
            turtle.fd(value1)
            turtle.right(90)
            turtle.fd(value2)
            turtle.right(90)
            turtle.fd(value1)
            turtle.right(90)
            turtle.fd(offset2)
            turtle.right(90)
            turtle.setheading(direccion)
            turtle.penup()
            turtle.back(offset1)
            turtle.pendown()
        elif(instruccion == 29):
            turtle.left(int(getMemoryValue(cuadruploActual[3])))
        #
        # elif(instruccion == 29):
        #     side1=int(getMemoryValue(cuadruploActual[1]))
        #     side2=int(getMemoryValue(cuadruploActual[2]))
        #     side3=int(getMemoryValue(cuadruploActual[3]))
        #     if((side1+side2>side3) and (side1+side3 > side2) and (side2 + side3 > side1)):
        #         cos3 = -((side3*side3) - (side1*side1) - (side2*side2))/(2*side1*side2)
        #         ang3 = math.acos(cos3)
        #         cos2 = -((side2*side2) - (side1*side1) - (side3*side3))/(2*side1*side3)
        #         ang2 = math.acos(cos2)
        #         ang2 = (ang2 * 180) / math.pi
        #         ang3 = (ang3 * 180) / math.pi
        #         ang1 = 180 - ang2 - ang3
        #         direccion = turtle.heading()
        #         s = (side1 + side2 + side3)/2
        #         area = math.sqrt(s*(s-side1)*(s-side2)*(s-side3))
        #         base = max(side1,side2,side3)
        #         h = (area*2)/base
        #         turtle.penup()
        #         turtle.fd(h/2)
        #         turtle.pendown()
        #         if(base != side1 and base != side2):
        #             print ang1,ang2,ang3
        #             turtle.left(180 - (ang3/2))
        #             turtle.fd(side1)
        #             turtle.left(180-ang2)
        #             turtle.fd(side3)
        #             turtle.left(180 - ang1)
        #             turtle.fd(side2)
        #             turtle.left(180 - (ang3 / 2))
        #
        #         elif(base != side2 and base != side3):
        #             print ang1, ang2, ang3
        #             turtle.left(180 - (ang3 / 2))
        #             turtle.fd(side2)
        #             turtle.left(180 - ang1)
        #             turtle.fd(side3)
        #             turtle.left(180 - ang2)
        #             turtle.fd(side1)
        #             turtle.left(180 - (ang3 / 2))
        #         else:
        #             print ang1, ang2, ang3
        #             turtle.left(180 - (ang3 / 2))
        #             turtle.fd(side1)
        #             turtle.left(180 - ang2)
        #             turtle.fd(side3)
        #             turtle.left(180 - ang1)
        #             turtle.fd(side2)
        #             turtle.left(180 - (ang3 / 2))
        #        turtle.setheading(direccion)
        #        turtle.back(h/2)
        #
        #     else:
        #         turtle.penup()
        #         turtle.back(250)
        #         turtle.pendown()
        #         turtle.write("GIVEN SIDES OF THE TRIANGLE ARE WRONG", font=("Arial", 16, "normal"))
        cuadruploActual = cuadruplos[currentPointer]
        currentPointer += 1
    turtle.getscreen()._root.mainloop()



run()
