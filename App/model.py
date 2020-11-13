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

    analyzer['graph'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=10000,
                                              comparefunction=compareStations)
    return analyzer


# Funciones para agregar informacion al grafo

def addTrip(analyzer, trip):
    origin = trip['start station id']
    destination = trip['end station id']
    duration = int(trip['tripduration'])
    addStation(analyzer, origin)
    addStation(analyzer, destination)
    addConnection(analyzer, origin, destination, duration)
    addTripStop(analyzer, trip)
    return analyzer

def addStation(analyzer, stationid):
    if not gr.containsVertex(analyzer["graph"], stationid):
            gr.insertVertex(analyzer["graph"], stationid)
    return analyzer

def addTripStop(analyzer, route):
    entry = m.get(analyzer['stations'], route["end station id"])
    if entry is None:
        lststations = lt.newList("ARRAY_LIST", cmpfunction=compareroutes)
        lt.addLast(lststations, route["end station name"])
        lt.addLast(lststations, route["end station latitude"])
        lt.addLast(lststations, route["end station longitude"])
        m.put(analyzer['stations'], route['end station id'], lststations)
    else:
        lststations = entry['value']
        info = route['end station name']
        if not lt.isPresent(lststations, info):
            lt.addLast(lststations, info)
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
                stop = stack.pop(LT)
                maxIni -= int(stop["size"])*20
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

# ==============================
# Funciones Helper
# ==============================

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
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1