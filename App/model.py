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

    analyzer['stations'] = m.newMap(numelements=14000,
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
    return analyzer

def addStation(analyzer, stationid):
    if not gr.containsVertex(analyzer["graph"], stationid):
            gr.insertVertex(analyzer["graph"], stationid)
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
    return scc.stronglyConnected(analyzer["components"], station1, station2)

def totalEdges(analyzer):
    return gr.numEdges(analyzer['graph'])

def totalStations(analyzer):
    return gr.numVertices(analyzer['graph'])

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