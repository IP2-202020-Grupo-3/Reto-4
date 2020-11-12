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

import config as cf
from App import model
import csv
import os

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicialización del catálogo
# ___________________________________________________

def init():
    analyzer = model.newAnalyzer()
    return analyzer
# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadTrips(analyzer):
    for filename in os.listdir(cf.data_dir):
        if filename.endswith('.csv'):
            print('Cargando archivo: ' + filename)
            loadFile(analyzer, filename)
    return analyzer

def loadFile(analyzer, tripfile):
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding="utf-8"),
                                delimiter=",")
    for trip in input_file:
        model.addTrip(analyzer, trip)
    return analyzer


# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def numSCC(graph, sc):
    return model.numSCC(graph, sc)

def sameCC(sc, station1, station2):
    return model.sameCC(sc, station1, station2)

def totalEdges(analyzer):
    return model.totalEdges(analyzer)

def totalStations(analyzer):
    return model.totalStations(analyzer)

def connectedComponents(analyzer):
    return model.connectedComponents(analyzer)
    
def minimumCostPaths(analyzer, initialStation):
    return model.minimumCostPaths(analyzer, initialStation)

def minimumCostPath(analyzer, destStation):
    return model.minimumCostPath(analyzer, destStation)

def hasPath(analyzer, destStation):
    return model.hasPath(analyzer, destStation)

def getPaths(analyzer, initStation, distanciaIni, distanciaFin):
    return model.getPaths(analyzer, initStation, distanciaIni, distanciaFin)