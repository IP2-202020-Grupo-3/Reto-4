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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.DataStructures import edge as ed
from DISClib.Algorithms.Graphs import bfs
from DISClib.ADT import stack
assert config
from math import radians, cos, sin, asin, sqrt

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

def newAnalyzer():
    """ Inicializa el analizador

   stations: Tabla de hash para guardar los vertices del grafo
   graph: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    analyzer = {
                'stations': None,
                'graph': None,
                'components': None,
                'paths': None
                    }

    analyzer['stations'] = m.newMap(numelements=2000,
                                     maptype='PROBING',
                                     comparefunction=compareStations)

    analyzer['stationsIni'] = m.newMap(numelements=2000,
                                     maptype='PROBING',
                                     comparefunction=compareStations)

    analyzer['graph'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=10000,
                                              comparefunction=compareStations)
    return analyzer


# Funciones para agregar información al grafo

def addTrip(analyzer, trip):
    origin = trip['start station id']
    destination = trip['end station id']
    duration = int(trip['tripduration'])
    addStation(analyzer, origin)
    addStation(analyzer, destination)
    addConnection(analyzer, origin, destination, duration)
    addTripStop(analyzer, trip)
    addTripStart(analyzer, trip)
    return analyzer

def addStation(analyzer, stationid):
    if not gr.containsVertex(analyzer["graph"], stationid):
            gr.insertVertex(analyzer["graph"], stationid)
    return analyzer

def addTripStop(analyzer, route):
    entry = m.get(analyzer['stations'], route["end station id"])
    edades = {"0-10":0, "11-20":0, "21-30":0, "31-40":0, "41-50":0, "51-60":0, "60+":0}
    if entry is None:
        lststations = lt.newList("ARRAY_LIST", cmpfunction=compareroutes)
        cantViajes = {"cantidad viajes": 1}
        lt.addLast(lststations, route["end station name"])
        lt.addLast(lststations, route["end station latitude"])
        lt.addLast(lststations, route["end station longitude"])
        lt.addLast(lststations, edades)
        lt.addLast(lststations, cantViajes)
        if 2020-int(route["birth year"]) >=0 and 2020-int(route["birth year"]) <= 10:
            lststations["elements"][3]["0-10"] += 1
        elif 2020-int(route["birth year"]) >=11 and 2020-int(route["birth year"]) <= 20:
            lststations["elements"][3]["11-20"] += 1
        elif 2020-int(route["birth year"]) >=21 and 2020-int(route["birth year"]) <= 30:
            lststations["elements"][3]["21-30"] += 1
        elif 2020-int(route["birth year"]) >=31 and 2020-int(route["birth year"]) <= 40:
            lststations["elements"][3]["31-40"] += 1
        elif 2020-int(route["birth year"]) >=41 and 2020-int(route["birth year"]) <= 50:
            lststations["elements"][3]["41-50"] += 1
        elif 2020-int(route["birth year"]) >=51 and 2020-int(route["birth year"]) <= 60:
            lststations["elements"][3]["51-60"] += 1
        elif 2020-int(route["birth year"]) >60:
            lststations["elements"][3]["60+"] += 1
        m.put(analyzer['stations'], route['end station id'], lststations)
    else:
        lststations = entry['value']
        if 2020-int(route["birth year"]) >=0 and 2020-int(route["birth year"]) <= 10:
            lststations["elements"][3]["0-10"] += 1
        elif 2020-int(route["birth year"]) >=11 and 2020-int(route["birth year"]) <= 20:
            lststations["elements"][3]["11-20"] += 1
        elif 2020-int(route["birth year"]) >=21 and 2020-int(route["birth year"]) <= 30:
            lststations["elements"][3]["21-30"] += 1
        elif 2020-int(route["birth year"]) >=31 and 2020-int(route["birth year"]) <= 40:
            lststations["elements"][3]["31-40"] += 1
        elif 2020-int(route["birth year"]) >=41 and 2020-int(route["birth year"]) <= 50:
            lststations["elements"][3]["41-50"] += 1
        elif 2020-int(route["birth year"]) >=51 and 2020-int(route["birth year"]) <= 60:
            lststations["elements"][3]["51-60"] += 1
        elif 2020-int(route["birth year"]) >60:
            lststations["elements"][3]["60+"] += 1
        lststations["elements"][4]["cantidad viajes"] +=1
    return analyzer

def addTripStart(analyzer, route):
    entry = m.get(analyzer['stationsIni'], route["start station id"])
    edades = {"0-10":0, "11-20":0, "21-30":0, "31-40":0, "41-50":0, "51-60":0, "60+":0}
    if entry is None:
        lststations = lt.newList("ARRAY_LIST", cmpfunction=compareroutes)
        cantViajes = {"cantidad viajes": 1}
        lt.addLast(lststations, route["start station name"])
        lt.addLast(lststations, route["start station latitude"])
        lt.addLast(lststations, route["start station longitude"])
        lt.addLast(lststations, edades)
        lt.addLast(lststations, cantViajes)
        if 2020-int(route["birth year"]) >=0 and 2020-int(route["birth year"]) <= 10:
            lststations["elements"][3]["0-10"] += 1
        elif 2020-int(route["birth year"]) >=11 and 2020-int(route["birth year"]) <= 20:
            lststations["elements"][3]["11-20"] += 1
        elif 2020-int(route["birth year"]) >=21 and 2020-int(route["birth year"]) <= 30:
            lststations["elements"][3]["21-30"] += 1
        elif 2020-int(route["birth year"]) >=31 and 2020-int(route["birth year"]) <= 40:
            lststations["elements"][3]["31-40"] += 1
        elif 2020-int(route["birth year"]) >=41 and 2020-int(route["birth year"]) <= 50:
            lststations["elements"][3]["41-50"] += 1
        elif 2020-int(route["birth year"]) >=51 and 2020-int(route["birth year"]) <= 60:
            lststations["elements"][3]["51-60"] += 1
        elif 2020-int(route["birth year"]) >60:
            lststations["elements"][3]["60+"] += 1
        m.put(analyzer['stationsIni'], route['start station id'], lststations)
    else:
        lststations = entry['value']
        if 2020-int(route["birth year"]) >=0 and 2020-int(route["birth year"]) <= 10:
            lststations["elements"][3]["0-10"] += 1
        elif 2020-int(route["birth year"]) >=11 and 2020-int(route["birth year"]) <= 20:
            lststations["elements"][3]["11-20"] += 1
        elif 2020-int(route["birth year"]) >=21 and 2020-int(route["birth year"]) <= 30:
            lststations["elements"][3]["21-30"] += 1
        elif 2020-int(route["birth year"]) >=31 and 2020-int(route["birth year"]) <= 40:
            lststations["elements"][3]["31-40"] += 1
        elif 2020-int(route["birth year"]) >=41 and 2020-int(route["birth year"]) <= 50:
            lststations["elements"][3]["41-50"] += 1
        elif 2020-int(route["birth year"]) >=51 and 2020-int(route["birth year"]) <= 60:
            lststations["elements"][3]["51-60"] += 1
        elif 2020-int(route["birth year"]) >60:
            lststations["elements"][3]["60+"] += 1
        lststations["elements"][4]["cantidad viajes"] +=1
    return analyzer

def addConnection(analyzer, origin, destination, duration):
    edge = gr.getEdge(analyzer["graph"], origin, destination)
    if edge is None:
        gr.addEdge(analyzer["graph"], origin, destination, duration)
    else:
        ed.updateAverageWeight(edge, duration) 
    return analyzer

# ==============================
# Funciones de consulta
# ==============================
def connectedComponents(analyzer):
    analyzer['components'] = scc.KosarajuSCC(analyzer['graph'])
    return scc.connectedComponents(analyzer['components'])

def sameCC(analyzer, station1, station2):
    vert1 = gr.containsVertex(analyzer["graph"], station1)
    vert2 = gr.containsVertex(analyzer["graph"], station2)
    if vert1 is False and vert2 is False:
        return "0"
    elif vert1 is False:
        return "1"
    elif vert2 is False:
        return "2"
    else:
        return scc.stronglyConnected(analyzer["components"], station1, station2)

def totalEdges(analyzer):
    return gr.numEdges(analyzer['graph'])

def totalStations(analyzer):
    return gr.numVertices(analyzer['graph'])

def getPaths(analyzer, initStation, distanciaIni, distanciaFin):
    if gr.containsVertex(analyzer["graph"], initStation) == True:
        LT = lt.newList("ARRAY_LIST")
        finlist = lt.newList("ARRAY_LIST")
        adj = gr.adjacents(analyzer["graph"], initStation)
        connectedComponents(analyzer)
        for element in adj["elements"]:
            val = sameCC(analyzer, initStation, element)
            if val == True:
                ini = 0
                fin = 1
                peso = 0
                analyzer['paths'] = bfs.BreadthFisrtSearch(analyzer["graph"], element)
                camino = bfs.pathTo(analyzer["paths"], initStation)
                lt.addFirst(camino, initStation)
                while ini < lt.size(camino)-1:
                    arco = gr.getEdge(analyzer["graph"], camino["elements"][ini], camino["elements"][fin])
                    peso += float(arco["weight"])
                    ini +=1
                    fin +=1
                camino["distance"] = peso
                lt.addLast(LT, camino)
        if LT is not None:
            minIni = distanciaIni*60
            maxIni = distanciaFin*60
            while (not stack.isEmpty(LT)):
                maxIni = distanciaFin*60
                stop = stack.pop(LT)
                maxIni -= int(stop["size"]-1)*20
                if stop["distance"] >= minIni and stop["distance"] <= maxIni: 
                    lt.addLast(finlist, stop)                  
        return finlist

def resistancePath(analyzer, initStation, resistance):
    if gr.containsVertex(analyzer["graph"], initStation) == True:
        analyzer['paths'] = bfs.BreadthFisrtSearch(analyzer["graph"], initStation)
        vertices = gr.vertices(analyzer["graph"])
        iterador = it.newIterator(vertices)
        LT = lt.newList("ARRAY_LIST")
        finlist = lt.newList("ARRAY_LIST")
        while it.hasNext(iterador):
            vertice = it.next(iterador)
            if bfs.hasPathTo(analyzer["paths"], vertice):
                caminos = bfs.pathTo(analyzer["paths"], vertice)
                ini = 0
                fin = 1
                peso = 0
                while ini < lt.size(caminos)-1:
                    arco = gr.getEdge(analyzer["graph"], caminos["elements"][ini], caminos["elements"][fin])
                    peso += float(arco["weight"])
                    ini +=1
                    fin +=1
                caminos["distance"] = peso
                lt.addLast(LT, caminos)
        if LT is not None:
            resistenciamin = resistance*60
            while (not stack.isEmpty(LT)):
                stop = stack.pop(LT)
                if float(stop["distance"]) <= resistenciamin and str(stop["elements"]) not in finlist:
                    lt.addLast(finlist, stop)
        return finlist
        
def estCrit(analyzer):
    vertices = gr.vertices(analyzer["graph"])
    dicc1 = {}
    dicc2 = {}
    dicc3 = {}
    entrada = lt.newList("ARRAY_LIST")
    salida = lt.newList("ARRAY_LIST")
    menores = lt.newList("ARRAY_LIST")
    iterador = it.newIterator(vertices)
    while it.hasNext(iterador):
        vertice = it.next(iterador)
        num = m.get(analyzer["stations"], vertice)
        dicc1[vertice] = num["value"]["elements"][4]["cantidad viajes"]
        num2 = m.get(analyzer["stationsIni"], vertice)
        if num2 is None:
            num2 = 0
            dicc2[vertice] = 0
            num3 = num["value"]["elements"][4]["cantidad viajes"]
        else:
            dicc2[vertice] = num2["value"]["elements"][4]["cantidad viajes"]
            num3 = int(num["value"]["elements"][4]["cantidad viajes"]) + int(num2["value"]["elements"][4]["cantidad viajes"])
        dicc3[vertice] = num3

    for i in range(3):
        llavesEntrada = list(dicc1.keys())
        valoresEntrada = list(dicc1.values())
        mayorEntrada = max(valoresEntrada)
        entradaMax = str(llavesEntrada[valoresEntrada.index(mayorEntrada)])
        lt.addLast(entrada, entradaMax)
        dicc1.pop(entradaMax)

    for i in range(3):
        llavesSalida = list(dicc2.keys())
        valoresSalida = list(dicc2.values())
        mayorSalida = max(valoresSalida)
        salidaMax = str(llavesSalida[valoresSalida.index(mayorSalida)])
        lt.addLast(salida, salidaMax)
        dicc2.pop(salidaMax)
    
    for i in range(3):
        llavesMenores = list(dicc3.keys())
        valoresMenores = list(dicc3.values())
        mayorMenores = min(valoresMenores)
        menoresMax = str(llavesMenores[valoresMenores.index(mayorMenores)])
        lt.addLast(menores, menoresMax)
        dicc3.pop(menoresMax)
    
    return entrada, salida, menores




def recomendador(analyzer, edad):
    if int(edad) >=0 and int(edad) <= 10:
        edad = "0-10"
    elif int(edad) >=11 and int(edad) <= 20:
       edad = "11-20"
    elif int(edad) >=21 and int(edad) <= 30:
        edad = "21-30"
    elif int(edad) >=31 and int(edad) <= 40:
        edad = "31-40"
    elif int(edad) >=41 and int(edad) <= 50:
        edad = "41-50"
    elif int(edad) >=51 and int(edad) <= 60:
        edad = "51-60"
    elif int(edad) >60:
        edad = "60+"
    dicc1 = {}
    dicc2 = {}
    vertices = gr.vertices(analyzer["graph"])
    iterador = it.newIterator(vertices)
    if edad == "0-10":
        while it.hasNext(iterador):
            vertice = it.next(iterador)
            estFin = m.get(analyzer["stations"], vertice)
            estIni = m.get(analyzer["stationsIni"], vertice)
            if estIni is not None:
                key = estFin["key"]
                dicc1[key] = estIni["value"]["elements"][3]["0-10"]
            if estFin is not None:
                key = estFin["key"]
                dicc2[key] = estFin["value"]["elements"][3]["0-10"]
        
        llavesInicial = list(dicc1.keys())
        valoresInicial = list(dicc1.values())
        mayorInicial = max(valoresInicial)
        inicialMax = str(llavesInicial[valoresInicial.index(mayorInicial)])

        llavesFinal = list(dicc2.keys())
        valoresFinal = list(dicc2.values())
        mayorFinal = max(valoresFinal)
        finalMax = str(llavesFinal[valoresFinal.index(mayorFinal)])

        minimumCostPaths(analyzer, inicialMax)
        
        path = minimumCostPath(analyzer, finalMax)

        return inicialMax, finalMax, path

    elif edad == "11-20":
        while it.hasNext(iterador):
            vertice = it.next(iterador)
            estFin = m.get(analyzer["stations"], vertice)
            estIni = m.get(analyzer["stationsIni"], vertice)
            if estIni is not None:
                key = estFin["key"]
                dicc1[key] = estIni["value"]["elements"][3]["11-20"]
            if estFin is not None:
                key = estFin["key"]
                dicc2[key] = estFin["value"]["elements"][3]["11-20"]
        
        llavesInicial = list(dicc1.keys())
        valoresInicial = list(dicc1.values())
        mayorInicial = max(valoresInicial)
        inicialMax = str(llavesInicial[valoresInicial.index(mayorInicial)])

        llavesFinal = list(dicc2.keys())
        valoresFinal = list(dicc2.values())
        mayorFinal = max(valoresFinal)
        finalMax = str(llavesFinal[valoresFinal.index(mayorFinal)])

        minimumCostPaths(analyzer, inicialMax)
        
        path = minimumCostPath(analyzer, finalMax)

        return inicialMax, finalMax, path

    elif edad == "21-30":
        while it.hasNext(iterador):
            vertice = it.next(iterador)
            estFin = m.get(analyzer["stations"], vertice)
            estIni = m.get(analyzer["stationsIni"], vertice)
            if estIni is not None:
                key = estFin["key"]
                dicc1[key] = estIni["value"]["elements"][3]["21-30"]
            if estFin is not None:
                key = estFin["key"]
                dicc2[key] = estFin["value"]["elements"][3]["21-30"]
        
        llavesInicial = list(dicc1.keys())
        valoresInicial = list(dicc1.values())
        mayorInicial = max(valoresInicial)
        inicialMax = str(llavesInicial[valoresInicial.index(mayorInicial)])

        llavesFinal = list(dicc2.keys())
        valoresFinal = list(dicc2.values())
        mayorFinal = max(valoresFinal)
        finalMax = str(llavesFinal[valoresFinal.index(mayorFinal)])

        minimumCostPaths(analyzer, inicialMax)
        
        path = minimumCostPath(analyzer, finalMax)

        return inicialMax, finalMax, path

    elif edad == "31-40":
        while it.hasNext(iterador):
            vertice = it.next(iterador)
            estFin = m.get(analyzer["stations"], vertice)
            estIni = m.get(analyzer["stationsIni"], vertice)
            if estIni is not None:
                key = estFin["key"]
                dicc1[key] = estIni["value"]["elements"][3]["31-40"]
            if estFin is not None:
                key = estFin["key"]
                dicc2[key] = estFin["value"]["elements"][3]["31-40"]
        
        llavesInicial = list(dicc1.keys())
        valoresInicial = list(dicc1.values())
        mayorInicial = max(valoresInicial)
        inicialMax = str(llavesInicial[valoresInicial.index(mayorInicial)])

        llavesFinal = list(dicc2.keys())
        valoresFinal = list(dicc2.values())
        mayorFinal = max(valoresFinal)
        finalMax = str(llavesFinal[valoresFinal.index(mayorFinal)])

        minimumCostPaths(analyzer, inicialMax)
        
        path = minimumCostPath(analyzer, finalMax)

        return inicialMax, finalMax, path

    elif edad == "41-50":
        while it.hasNext(iterador):
            vertice = it.next(iterador)
            estFin = m.get(analyzer["stations"], vertice)
            estIni = m.get(analyzer["stationsIni"], vertice)
            if estIni is not None:
                key = estFin["key"]
                dicc1[key] = estIni["value"]["elements"][3]["41-50"]
            if estFin is not None:
                key = estFin["key"]
                dicc2[key] = estFin["value"]["elements"][3]["41-50"]
        
        llavesInicial = list(dicc1.keys())
        valoresInicial = list(dicc1.values())
        mayorInicial = max(valoresInicial)
        inicialMax = str(llavesInicial[valoresInicial.index(mayorInicial)])

        llavesFinal = list(dicc2.keys())
        valoresFinal = list(dicc2.values())
        mayorFinal = max(valoresFinal)
        finalMax = str(llavesFinal[valoresFinal.index(mayorFinal)])

        minimumCostPaths(analyzer, inicialMax)
        
        path = minimumCostPath(analyzer, finalMax)

        return inicialMax, finalMax, path

    elif edad == "51-60":
        while it.hasNext(iterador):
            vertice = it.next(iterador)
            estFin = m.get(analyzer["stations"], vertice)
            estIni = m.get(analyzer["stationsIni"], vertice)
            if estIni is not None:
                key = estFin["key"]
                dicc1[key] = estIni["value"]["elements"][3]["51-60"]
            if estFin is not None:
                key = estFin["key"]
                dicc2[key] = estFin["value"]["elements"][3]["51-60"]
        
        llavesInicial = list(dicc1.keys())
        valoresInicial = list(dicc1.values())
        mayorInicial = max(valoresInicial)
        inicialMax = str(llavesInicial[valoresInicial.index(mayorInicial)])

        llavesFinal = list(dicc2.keys())
        valoresFinal = list(dicc2.values())
        mayorFinal = max(valoresFinal)
        finalMax = str(llavesFinal[valoresFinal.index(mayorFinal)])

        minimumCostPaths(analyzer, inicialMax)
        
        path = minimumCostPath(analyzer, finalMax)

        return inicialMax, finalMax, path

    elif edad == "60+":
        while it.hasNext(iterador):
            vertice = it.next(iterador)
            estFin = m.get(analyzer["stations"], vertice)
            estIni = m.get(analyzer["stationsIni"], vertice)
            if estIni is not None:
                key = estFin["key"]
                dicc1[key] = estIni["value"]["elements"][3]["60+"]
            if estFin is not None:
                key = estFin["key"]
                dicc2[key] = estFin["value"]["elements"][3]["60+"]
        
        llavesInicial = list(dicc1.keys())
        valoresInicial = list(dicc1.values())
        mayorInicial = max(valoresInicial)
        inicialMax = str(llavesInicial[valoresInicial.index(mayorInicial)])

        llavesFinal = list(dicc2.keys())
        valoresFinal = list(dicc2.values())
        mayorFinal = max(valoresFinal)
        finalMax = str(llavesFinal[valoresFinal.index(mayorFinal)])

        minimumCostPaths(analyzer, inicialMax)
        
        path = minimumCostPath(analyzer, finalMax)

        return inicialMax, finalMax, path
                      

def minimumCostPaths(analyzer, initialStation):
    if gr.containsVertex(analyzer["graph"], initialStation) == True:
        analyzer['paths'] = djk.Dijkstra(analyzer['graph'], initialStation)
        return analyzer
    else:
        return "0"

def hasPath(analyzer, destStation):
    return djk.hasPathTo(analyzer['paths'], destStation)

def minimumCostPath(analyzer, destStation):
    path = djk.pathTo(analyzer['paths'], destStation)
    return path

def rutaTuris(analyzer, latOri, longOri, latDest, longDest):
    dicc1 = {}
    dicc2 = {}
    vertices = gr.vertices(analyzer["graph"])
    iterador = it.newIterator(vertices)
    while it.hasNext(iterador):
        vertice = it.next(iterador)
        estIni = m.get(analyzer["stations"], vertice)
        distanciaOri = distance(latOri, float(estIni["value"]["elements"][1]), longOri, float(estIni["value"]["elements"][2]))
        distanciaDest = distance(latDest, float(estIni["value"]["elements"][1]), longDest, float(estIni["value"]["elements"][2]))
        dicc1[vertice] = distanciaOri
        dicc2[vertice] = distanciaDest

    llavesInicial = list(dicc1.keys())
    valoresInicial = list(dicc1.values())
    mayorInicial = min(valoresInicial)
    inicialMin = str(llavesInicial[valoresInicial.index(mayorInicial)])

    llavesFinal = list(dicc2.keys())
    valoresFinal = list(dicc2.values())
    mayorFinal = min(valoresFinal)
    finalMin = str(llavesFinal[valoresFinal.index(mayorFinal)])

    minimumCostPaths(analyzer, inicialMin)

    path = minimumCostPath(analyzer, finalMin)

    return inicialMin, finalMin, path

# ==============================
# Funciones Helper
# ==============================

def distance(lat1, lat2, lon1, lon2): 
      
    # The math module contains a function named 
    # radians which converts from degrees to radians. 
    lon1 = radians(lon1) 
    lon2 = radians(lon2) 
    lat1 = radians(lat1) 
    lat2 = radians(lat2) 
       
    # Haversine formula  
    dlon = lon2 - lon1  
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  
    c = 2 * asin(sqrt(a))  
     
    # Radius of earth in kilometers. Use 3956 for miles 
    r = 6371
       
    # calculate the result 
    return(c * r * 1.609344)

# ==============================
# Funciones de Comparación
# ==============================

def compareStations(st1, st2):
    est = st2['key']
    if (st1 == est):
        return 0
    elif (st1 > est):
        return 1
    else:
        return -1

def compareroutes(route1, route2):
    if type(route1) is dict:
        route1 = str(route1)
    elif type(route2) is dict:
        route2 = str(route2)
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1