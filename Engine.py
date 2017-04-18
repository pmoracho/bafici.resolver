# -*- coding: utf-8 -*-

# Copyright (c) 20014 Patricio Moracho <pmoracho@gmail.com>
#
# Engine.py
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 3 of the GNU General Public License
# as published by the Free Software Foundation. A copy of this license should
# be included in the file GPL-3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
import csv
import os
import sys
import itertools
import time
from collections import Counter

from Object import Object
from Ubicacion import Ubicacion
from Ubicaciones import Ubicaciones
from Distancia import Distancia
from Distancias import Distancias
from Tema import Tema
from Temas import Temas
from Hito import Hito
from Hitos import Hitos
from Combinacion import Combinacion
from Combinaciones import Combinaciones


__author__ 		= "Patricio Moracho <pmoracho@gmail.com>"
__copyright__ 	= "Copyright (C) 2014 Patricio Moracho"
__license__   	= 'GPL v3'
__copyright__ 	= "2014, %s" % (__author__)
__version__ 	= "1.1"
__date__ 		= "2014/06/24 13:42:03"
__magic__ 		= ""


#################################################################################################################################################
# Engine
#################################################################################################################################################
class Engine(Object):

	"""
	Motor principal de la aplicación
	"""

	def __init__(self):

		Object.__init__(self)

		self.Temas				= Temas("Todos")
		self.TemasSeleccion		= Temas("Seleccion")
		self.Ubicaciones		= Ubicaciones()
		self.Distancias			= Distancias()
		self.Combinaciones		= Combinaciones()
		self.Hitos				= Hitos(self.Distancias)
		self.observers 			= []
		self.HoraDesdeFiltro 	= ""
		self.HoraHastaFiltro 	= ""
		self.algoritmos 		= [
								("MT0-Todas las combinaciones", "generarCombinaciones_MT0", True),
								("MT1-Randomización de hitos", "generarCombinaciones_MT1", True),
								("MT2-Hitos ordenados por fecha", "generarCombinaciones_MT2", True),
								("MT3-Orden por combinabilidad (desc)", "generarCombinaciones_MT3", True),
								("MT4-Orden por combinabilidad (asc)", "generarCombinaciones_MT4", True),
								("MT5-Orden por combinabilidad de temas (desc)", "generarCombinaciones_MT5", True)
								]
		self.algoritmoDefault 	= "MT3-Orden por combinabilidad (desc)"

		self.__load_data()

	def register(self, observer):
		if observer not in self.observers:
			self.observers.append(observer)

	def unregister(self, observer):
		if observer in self.observers:
			self.observers.remove(observer)

	def unregister_all(self):
		if self.observers:
			del self.observers[:]

	def update_observers(self, *args, **kwargs):
		for observer in self.observers:
			observer.update(*args, **kwargs)

	def getAlgoritmosHabilitados(self):
		return [algoritmo for (algoritmo, funcion, habilitado) in self.algoritmos if habilitado]

	def setfilter(self, tipofiltro, valor):

		if tipofiltro == "horadesde":
			self.HoraDesdeFiltro = valor
		elif tipofiltro == "horahasta":
			self.HoraHastaFiltro = valor

	def __load_data(self):
		"""
		Load internal data
		"""
		self.__csv_dict_reader(self.__find_data_file("temas.csv"),			"temas")
		self.__csv_dict_reader(self.__find_data_file("ubicaciones.csv"),	"ubicaciones")
		self.__csv_dict_reader(self.__find_data_file("hitos.csv"),			"hitos")
		self.__csv_dict_reader(self.__find_data_file("distancias.csv"),		"distancias")

	def __csv_dict_reader(self, filename, tipo):
		"""
		Read a CSV file using csv.DictReader
		"""
		try:
			with open(filename) as file_obj:
				reader = csv.DictReader(file_obj, delimiter=';')
				for line in reader:
					if tipo == "temas":
						self.addTema(line["Codigo"], line["Nombre"], line["Info"], int(line["Duracion"]))
					elif tipo == "ubicaciones":
						self.addUbicacion(line["Codigo"], line["Nombre"], line["Barrio"])
					elif tipo == "hitos":
						self.addHito(line["CodigoTema"], line["CodigoUbicacion"], int(line["Inicio"]), line["FechaHora"], line["Fecha"], line["Hora"])
					elif tipo == "distancias":
						self.addDistancia(line["Origen"], line["Destino"], int(line["Distancia"]))
		except IOError:
			raise IOError("Imposible abrir el archivo de %s en '%s'" % (tipo, filename))

	def __find_data_file(self, filename):
		"""
		Define of data path
		"""
		if getattr(sys, 'frozen', False):
			# The application is frozen
			datadir = os.path.join(os.path.dirname(sys.executable), "data")
		else:
			# The application is not frozen
			# Change this bit to match where you store your data files:
			datadir = os.path.join(os.path.dirname(__file__), "data")

		return os.path.join(datadir, filename)

	def addTema(self, codigo, nombre, info, duracion):
		self.Temas.add(Tema(codigo, nombre, info, duracion))

	def addTemaSeleccion(self, codigo):
		t = self.Temas.getbycodigo(codigo)
		if t is not None:
			if t not in self.TemasSeleccion:
				self.TemasSeleccion.add(t)

	def addUbicacion(self, codigo, nombre, barrio):
		self.Ubicaciones.add(Ubicacion(codigo, nombre, barrio))

	def addDistancia(self, codigoubicacionorigen, codigoubicaciondestino, distancia):

		uo = self.Ubicaciones.getbycodigo(codigoubicacionorigen)
		ud = self.Ubicaciones.getbycodigo(codigoubicaciondestino)
		self.Distancias.add(Distancia(uo, ud, distancia))

	def addHito(self, codigotema, codigoubicacion, inicio, fechahora, fecha, hora):

		t = self.Temas.getbycodigo(codigotema)
		u = self.Ubicaciones.getbycodigo(codigoubicacion)

		h = Hito(t, u, inicio, fechahora, fecha, hora)
		h.nro = len(self.Hitos) + 1

		self.Hitos.add(h)

	"""
	def generarDistancias(self):

		dd=Distancias()
		#for i in itertools.permutations(self.Ubicaciones, 2):
		for i in itertools.product(self.Ubicaciones, repeat=2):

			(uo,ud) = i
			distancia = 0

			if uo == ud:
				distancia = 1
			elif uo.barrio == ud.barrio:
				distancia = 10
			elif ( "Caballito", "Recoleta") in ( (uo.barrio,ud.barrio), (ud.barrio,uo.barrio) ):
				distancia = 90
			elif ( "Caballito", "La Boca") in ( (uo.barrio,ud.barrio), (ud.barrio,uo.barrio) ):
				distancia = 90
			elif ( "Centro", "La Boca") in ( (uo.barrio,ud.barrio), (ud.barrio,uo.barrio) ):
				distancia = 60
			elif ( "Barrio Norte", "Belgrano") in ( (uo.barrio,ud.barrio), (ud.barrio,uo.barrio) ):
				distancia = 100
			elif ( "La Boca", "Belgrano") in ( (uo.barrio,ud.barrio), (ud.barrio,uo.barrio) ):
				distancia = 120
			elif ( "Centro", "Belgrano") in ( (uo.barrio,ud.barrio), (ud.barrio,uo.barrio) ):
				distancia = 60
			elif ( "Caballito", "Belgrano") in ( (uo.barrio,ud.barrio), (ud.barrio,uo.barrio) ):
				distancia = 120
			elif ( "Recoleta", "Belgrano") in ( (uo.barrio,ud.barrio), (ud.barrio,uo.barrio) ):
				distancia = 90
			elif ( "Barrio Norte", "La Boca") in ( (uo.barrio,ud.barrio), (ud.barrio,uo.barrio) ):
				distancia = 90
			elif ( "Caballito", "Centro") in ( (uo.barrio,ud.barrio), (ud.barrio,uo.barrio) ):
				distancia = 60
			elif ( "Recoleta", "Centro") in ( (uo.barrio,ud.barrio), (ud.barrio,uo.barrio) ):
				distancia = 45
			elif ( "Barrio Norte", "Recoleta") in ( (uo.barrio,ud.barrio), (ud.barrio,uo.barrio) ):
				distancia = 30
			elif ( "Barrio Norte", "Centro") in ( (uo.barrio,ud.barrio), (ud.barrio,uo.barrio) ):
				distancia = 45
			elif ( "Barrio Norte", "Caballito") in ( (uo.barrio,ud.barrio), (ud.barrio,uo.barrio) ):
				distancia = 120
			elif ( "Recoleta", "La Boca") in ( (uo.barrio,ud.barrio), (ud.barrio,uo.barrio) ):
				distancia = 90

			dd.add(Distancia(uo, ud, distancia))

		dd.report()
		dd.csv()
	"""

	def HitosSeleccion(self):
		hitos_temas_seleccionados = self.Hitos.filterbytemas(self.TemasSeleccion)
		hitos_temas_seleccionados.sort()
		return hitos_temas_seleccionados

	def generarCombinaciones_MT0(self):
		"""
		Genera todas las permutaciones con los hitos de los temas seleccionados
		Por cada uno se verifica si es posible la combinación
		No usar, solo a modo de prueba, demora con 6 temas unos 14 minutos (menos de 1 minuto con el pypy).
		"""
		if len(self.TemasSeleccion) > 6:
			raise Exception("Lo sentimos, el agoritmo MT0 es de permutaciones clásico lo cual demora mucho, por lo que se permite solo intentar con 6 temas/peliculas")
			return

		i = 1
		hitos_temas_seleccionados = self.Hitos.filterbytemas(self.TemasSeleccion)
		for hitos in itertools.combinations(hitos_temas_seleccionados, len(self.TemasSeleccion)):
			self.update_observers("Probando combinación %d" % i)
			new = Combinacion(self.Distancias, self.HoraDesdeFiltro, self.HoraHastaFiltro)
			for h in hitos:
				if new.validhito(h):
					new.addhito(h)

			self.Combinaciones.add(new)
			i = i+1

	def generarCombinaciones_MT1(self, intentos=10):
		"""
		Algoritmo Moracho/Troglio (MT1)
		- Randomización total de los hitos
		"""
		for i in range(intentos):
			hitos_temas_seleccionados = self.Hitos.filterbytemas(self.TemasSeleccion).randomize()
			self.__generar_combinaciones(self.TemasSeleccion, hitos_temas_seleccionados, i)

	def generarCombinaciones_MT2(self, intentos=10):
		"""
		Algoritmo Moracho/Troglio (MT2)
		- Se arma una lista de hitos de los temas seleccionados ordenado todo por fecha de inicio
		"""
		hitos_temas_seleccionados = self.Hitos.filterbytemas(self.TemasSeleccion)
		hitos_temas_seleccionados.sort()

		self.__generar_combinaciones(self.TemasSeleccion, hitos_temas_seleccionados)

	def generarCombinaciones_MT3(self, intentos=10):
		"""
		Algoritmo Moracho/Troglio (MT3)
		- Probabilística
		Se arman todas las posibles combinaciones de 2 hitos
		De esta lista se arma una segunda lista con los hitos ordenados por la cantidad de combinaciones en las que participan (más combinables primero)
		Se itera por esta lista armando las combinaciones definitivas.
		"""
		hitos_temas_seleccionados = self.Hitos.filterbytemas(self.TemasSeleccion, True)

		hitos_parejas = []
		for pareja in itertools.combinations(hitos_temas_seleccionados, 2):
			new = Combinacion(self.Distancias, self.HoraDesdeFiltro, self.HoraHastaFiltro)
			if new.validhito(pareja[0]):
				new.addhito(pareja[0])
				if new.validhito(pareja[1]):
					hitos_parejas.append((pareja[0], pareja[1]))

		contador = Counter([x for sublist in hitos_parejas for x in sublist])
		hitos_combinables = [h for h, c in sorted(contador.items(), key=lambda tupla: tupla[1], reverse=True)]

		self.__generar_combinaciones(self.TemasSeleccion, hitos_combinables)

	def generarCombinaciones_MT4(self, intentos=10):
		"""
		Algoritmo Moracho/Troglio (MT3)
		- Probabilística
		Se arman todas las posibles combinaciones de 2 hitos
		De esta lista se arma una segunda lista con los hitos ordenados por la cantidad de combinaciones en las que participan (menos combinables primero)
		Se itera por esta lista armando las combinaciones definitivas.
		"""
		hitos_temas_seleccionados = self.Hitos.filterbytemas(self.TemasSeleccion, True)

		hitos_parejas = []
		for pareja in itertools.combinations(hitos_temas_seleccionados, 2):
			new = Combinacion(self.Distancias, self.HoraDesdeFiltro, self.HoraHastaFiltro)
			if new.validhito(pareja[0]):
				new.addhito(pareja[0])
				if new.validhito(pareja[1]):
					hitos_parejas.append((pareja[0], pareja[1]))

		contador = Counter([x for sublist in hitos_parejas for x in sublist])
		hitos_combinables = [h for h, c in sorted(contador.items(), key=lambda tupla: tupla[1], reverse=False)]

		self.__generar_combinaciones(self.TemasSeleccion, hitos_combinables)

	def generarCombinaciones_MT5(self, intentos=10):
		"""
		Algoritmo Moracho/Troglio (MT3)
		- Probabilística
		Se arman todas las posibles combinaciones de 2 hitos
		De esta lista se arma una segunda lista con los hitos ordenados por la cantidad de combinaciones en las que participan
		Se arma una lista de los hitos que son mas combinables
		Se itera por esta lista armando las combinaciones definitivas.
		"""
		hitos_temas_seleccionados = self.Hitos.filterbytemas(self.TemasSeleccion, True)

		hitos_parejas = []
		for pareja in itertools.combinations(hitos_temas_seleccionados, 2):
			new = Combinacion(self.Distancias, self.HoraDesdeFiltro, self.HoraHastaFiltro)
			if new.validhito(pareja[0]):
				new.addhito(pareja[0])
				if new.validhito(pareja[1]):
					hitos_parejas.append((pareja[0], pareja[1]))

		
		contador = Counter([x for sublist in hitos_parejas for x in sublist])

		temas = []
		for t in self.TemasSeleccion:
			temas.append((t, sum([ c for h,c in contador.items() if h.tema == t])))

		# Lista de los temas ordenados por combinabilidad
		hitos_combinables=[]
		for (t,c) in sorted(temas, key=lambda tupla: tupla[1], reverse=True):
			hitos_combinables.extend([ h for h,x in contador.items() if h.tema == t])
			"""
			l = [ h for h,x in contador.items() if h.tema == t]
			print(l)
			print(t)
			print("%d --> %s" % (c,t))
			"""
		"""
		for h in hitos_combinables:
			print(h)
		"""
		self.__generar_combinaciones(self.TemasSeleccion, hitos_combinables)

	"""
	def nuevalista(self, elemento_pivot, lista, combinables):

		newlista = []
		for elemento in lista:
			l = elemento_pivot ^ elemento
			if len(l) == 2:
				nuevo = elemento_pivot | l
				if l in combinables and nuevo not in newlista:
					newlista.append(nuevo)

		return newlista

	def generarCombinaciones_MT4(self, intentos=0):

		hitos_temas_seleccionados = self.Hitos.filterbytemas(self.TemasSeleccion, True)

		hitos_parejas = []

		for pareja in itertools.combinations(hitos_temas_seleccionados, 2):
			new = Combinacion(self.Distancias, self.HoraDesdeFiltro, self.HoraHastaFiltro)
			if new.validhito(pareja[0]):
				new.addhito(pareja[0])
				if new.validhito(pareja[1]):
					hitos_parejas.append({pareja[0], pareja[1]})

		self.update_observers("Total de parejas combinables %d" % (len(hitos_parejas)))
		combinar = list(hitos_parejas)
		newlista = []
		while True:
			for pivot in combinar:
				l = self.nuevalista(pivot, combinar, hitos_parejas)
				if len(l) != 0:
					newlista = []
					for e in l:
						if e not in newlista:
							newlista.append(e)

			self.update_observers("Total de combinaciones %d" % (len(newlista)))
			if len(l) == 0:
				break

			combinar = list(newlista)

		for hitos in newlista:
			new = Combinacion(self.Distancias, self.HoraDesdeFiltro, self.HoraHastaFiltro)
			for hito in hitos:
				if new.validhito(hito):
					new.addhito(hito)
			self.Combinaciones.add(new)
	"""

	def __generar_combinaciones(self, temas, hitos, intento=1):
		"""
		"""
		cant_temas = len(temas)
		cant_hitos = len(hitos)

		for i in range(cant_hitos):

			self.update_observers("Intento %d secuencia %d de %d" % (intento, i, cant_hitos))
			new = Combinacion(self.Distancias, self.HoraDesdeFiltro, self.HoraHastaFiltro)
			new.addhito(hitos[i])

			for j in range(i+1, cant_hitos):
				"""
				if cant_temas > cant_hitos - (i+1):
					break
				"""
				hito = hitos[j]
				if new.validhito(hito):
					new.addhito(hito)
					if len(new) == cant_temas:
						break

			self.Combinaciones.add(new)

	def generar_combinaciones(self, algoritmo):
		"""Genera la combinaciones de los hitos de los temas seleccionados según un algoritmo dado.

		Algoritmos definidos:
			- MT0-Todas las combinaciones
			- MT1-Randomización de hitos
			- MT2-Hitos ordenados por fecha
			- MT3-Orden por combinabilidad (desc)
			- MT4-Orden por combinabilidad (asc)
			- MT5-Orden por combinabilidad de temas (desc)

		params:
		======
		algoritmo

		Usage:
		======
		>>> Engine.generar_combinaciones("MT3-Orden por combinabilidad (desc)")
		>>> 
		"""
		for (nombre, funcion, habilitada) in list(self.algoritmos):
			if algoritmo == nombre:
				method = getattr(self, funcion)
				""""
				if hasattr(method, '__doc__'):
					print(getattr(method, '__doc__'))
				"""
				if habilitada:
					self.update_observers("Generando combinaciones (%s)" % algoritmo)

					start = time.time()
					method()
					end = time.time()

					self.update_observers("Combinación finalizada en %f segundos" % (end - start))
