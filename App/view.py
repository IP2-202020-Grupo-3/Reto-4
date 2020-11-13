"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
assert config
from DISClib.ADT import map as m

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________

initialStation = None
recursionLimit = 20000

# ___________________________________________________
#  Menú principal
# ___________________________________________________

"""
Menú principal
"""
def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información")
    print("3- Calcular componentes conectados")
    print("4- Calcular ruta turística circular")
    print("5- Pendiente")
    print("6- Calcular ruta turística por resistencia")
    print("7- Pendiente")
    print("0- Salir")
    print("*******************************************")

def optionTwo():
    print("\nCargando información de CitiBike....")
    controller.loadTrips(cont)
    numedges = controller.totalEdges(cont)
    numvertex = controller.totalStations(cont)
    print('Número de vértices: ' + str(numvertex))
    print('Número de arcos: ' + str(numedges))
    print('El límite de recursión actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    print('El límite de recursión se ajusta a: ' + str(recursionLimit))


def optionThree():
    print('El número de componentes fuertemente conectados es: ' +
          str(controller.connectedComponents(cont)))
    est1 = input("Ingrese la estación 1: ")
    est2 = input("Ingrese la estación 2: ")
    connect = controller.sameCC(cont, est1, est2)
    if connect == True:
        print("Las dos estaciones sí pertenecen al mismo cluster.")
    elif connect == False:
        print("Las dos estaciones no pertenecen al mismo cluster.")
    elif connect == "0":
        print("Ninguna de las estaciones ingresadas existe.")
    elif connect == "1":
        print("La estación 1 ingresada no existe.")
    else:
        print("La estación 2 ingresada no existe.")


def optionFour():
    destStation = input("Ingrese la estación a buscar: ")
    distanciaIni =float(input("Ingrese en minutos el tiempo mínimo disponible: "))
    distanciaFin = float(input("Ingrese en minutos el tiempo máximo disponible: "))
    path = controller.getPaths(cont, destStation, distanciaIni, distanciaFin)
    if path is not None:
        pathlen = stack.size(path)
        num = 1
        print('Se encontraron {0} rutas:\n'.format(pathlen))
        while (not stack.isEmpty(path)):
            stop = stack.pop(path)
            print("Ruta {0}: ".format(num))
            for statid in stop["elements"]:
                entry = m.get(cont["stations"], statid)
                print("{0} - ID: {1}".format(entry["value"]["elements"][0], statid))
            print("Tiempo en recorrer: {0} minutos\n".format((round(stop["distance"]/60, 2))))           
            num +=1
    else:
        print('No hay camino')


def optionFive():
    val = controller.minimumCostPaths(cont, initialStation)
    if val == "0":
        print("La estación ingresada no existe.")


def optionSix():
    initStation = input("Ingrese la estación inicial: ")
    resistencia = int(input("Ingrese su tiempo máximo de resistencia: "))
    path = controller.resistancePath(cont, initStation, resistencia)
    if path is not None:
        pathlen = stack.size(path)
        num = 1
        print('Se encontraron {0} rutas:'.format(pathlen))
        if pathlen >= 100:
            dec = input("¿Desea imprimir la información de todas las rutas? (tenga en cuenta de que se encontraron demasiadas rutas) [S/N]\nSi responde N se mostrarán solo las primeras 100: ")
            if dec == "S" or dec == "s":
                while (not stack.isEmpty(path)):
                    stop = stack.pop(path)
                    print("Ruta {0}: ".format(num))
                    for statid in stop["elements"]:
                        entry = m.get(cont["stations"], statid)
                        print("{0} - ID: {1}".format(entry["value"]["elements"][0], statid))
                    print("Tiempo en recorrer: {0} minutos\n".format((round(stop["distance"]/60, 2))))           
                    num +=1
            else:
                while num <=100:
                    stop = stack.pop(path)
                    print("Ruta {0}: ".format(num))
                    entry = m.get(cont["stations"], stop["elements"][stop["size"]-1])
                    print("Estación destino: {0} - ID: {1}".format(entry["value"]["elements"][0], stop["elements"][stop["size"]-1]))
                    print("Tiempo en recorrer: {0} minutos\n".format((round(stop["distance"]/60, 2))))
                    num +=1
        else:
            while (not stack.isEmpty(path)):
                    stop = stack.pop(path)
                    print("Ruta {0}: ".format(num))
                    for statid in stop["elements"]:
                        entry = m.get(cont["stations"], statid)
                        print("{0} - ID: {1}".format(entry["value"]["elements"][0], statid))
                    print("Tiempo en recorrer: {0} minutos\n".format((round(stop["distance"]/60, 2))))           
                    num +=1
    else:
        print('No hay camino')
    """
    path = controller.minimumCostPath(cont, destStation)
    if path is not None:
        pathlen = stack.size(path)
        print('El camino es de longitud: ' + str(pathlen))
        while (not stack.isEmpty(path)):
            stop = stack.pop(path)
            print(stop["first"])
            
    else:
        print('No hay camino')"""


def optionSeven():
    maxvert, maxdeg = controller.servedRoutes(cont)
    print('Estación: ' + maxvert + '  Total rutas servidas: '
          + str(maxdeg))


"""
Menú principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        cont = controller.init()

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 3:
        executiontime = timeit.timeit(optionThree, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 4:
        executiontime = timeit.timeit(optionFour, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 5:
        executiontime = timeit.timeit(optionFive, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 6:
        executiontime = timeit.timeit(optionSix, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 7:
        executiontime = timeit.timeit(optionSeven, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    else:
        sys.exit(0)
sys.exit(0)
