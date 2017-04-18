# -*- coding: utf-8 -*-
# Copyright (c) 20014 Patricio Moracho <pmoracho@gmail.com>
#
# Combinacion.py
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

__author__ = "Patricio Moracho (pmoracho@gmail.com)"
__version__ = "Revision: 1.1"
__date__ = "2014/06/24 13:42:03"

import datetime

from Object import Object
from Hitos import Hitos

#################################################################################################################################################
## Combinacion
#################################################################################################################################################


class Combinacion(Object):

	"""
	Clase para el manejo de una combinacion de Hitos / Proyecciones
	"""

	numero = 1

	def __init__(self, distancias, horadesde="", horahasta=""):

		Object.__init__(self)
		self.hitos = Hitos(distancias, horadesde, horahasta)
		self.horadesde = horadesde
		self.horahasta = horahasta
		self.descripcion = ""
		self.distancias = distancias
		self.numero = Combinacion.numero

		Combinacion.numero = Combinacion.numero + 1

	def __repr__(self):
		"""Class representation"""
		return self.__str__()

	def __str__(self):
		"""String representation"""
		return '[%s: (%d), %d, %s, %s, %s, %s]' % (self.__class__.__name__, self.id, self.numero, self.horadesde, self.horahasta, self.descripcion, Combinacion.__get_nice_string(self.hitos))

	def __get_nice_string(list):
		return "[" + ", ".join(str(item) for item in list) + "]"

	def __len__(self):
		"""Len of the list container"""
		return len(self.hitos)

	def __iter__(self):
		return iter(self.hitos)

	def reset_numero(self):
		Combinacion.numero = 0

	def addhito(self, hito):
		self.hitos.add(hito)
		self.hitos.sort()

	def validhito(self, hito):
		"""
		Valida un hito con relación al resto del histos en la combinación
		"""
		if not self.hitos:								# No hay ningún hito en la lista
			if not self.validtimefilter(hito):
				return False
		elif hito in self.hitos:						# El hito ya se enuentra en la lista
			return False
		elif self.existtema(hito):						# El tema del hito ya se existe en la lista
			return False
		elif not self.validtimefilter(hito):			# El hito está dentro de las horas en que se quiere participar del evento
			return False
		elif not self.validtimecombination(hito):		# El hito es posible de cumplir en función de los horarios y trayectos del resto de los hitos
			return False
		elif not self.validcambiosbarrio(hito):			# TODO: Cuantos cambios de barrio queremos hacer?
			return False
		elif not self.validcantidadhitosmax(hito):		# TODO: Cuantas películas por día
			return False
		return True

	def hitosdiferentes(self, combinacion):
		return list(set(self.hitos) - set(combinacion.hitos))

	def existtema(self, hito):
		"""
		Existe el tema en la lista de hitos?
		"""
		for h in self.hitos:
			if hito.tema == h.tema:
				return True
		return False

	def validcambiosbarrio(self, hito):
		"""
		Retorna verdader/falso si el hito no supera la cantidad de cambios de barrio/sedes solicitado
		"""
		return True

	def validcantidadhitosmax(self, hito):
		"""
		Retorna verdader/falso si el hito supera la cantidad de peliculas máxima por día solicitada
		"""
		return True

	def validtimefilter(self, hito):
		"""
		Retorna verdader/falso si el hito entra dentro del desde/hasta hora deseado
		"""
		if self.horadesde == "" and self.horahasta == "":
			return True
		else:

			hora = hito.fechahora[hito.fechahora.index(" / ")+3:]

			hora_hito = datetime.datetime.strptime(hora, "%H:%M")
			if self.horadesde != "":
				if self.isPrimerHitoDelDia(hito):
					hora_desde = datetime.datetime.strptime(self.horadesde, "%H:%M")
					if hora_desde > hora_hito:
						return False

			if self.horahasta != "":
				if self.isUltimoHitoDelDia(hito):
					hora_hasta = datetime.datetime.strptime(self.horahasta, "%H:%M")
					#print("%s --- %s =  %s --- %s" % (self.horahasta,str(hora_hasta),hora_hito, str(hora_hito)))
					if hora_hasta < hora_hito:
						return False

			return True

	def validtimecombination(self, hito):
		"""
		Valida si se puede insertar el hito en la combinación
		"""
		for i in range(-1, len(self.hitos)):
			if i == -1:
				inicial = None
				final = self.hitos[i+1]
			elif i == len(self.hitos)-1:
				inicial = self.hitos[i]
				final = None
			else:
				inicial = self.hitos[i]
				final = self.hitos[i+1]

			if self.validbetween(hito, inicial, final):
				return True

		return False

	def getDate(self, fechahora):
		#print("*%s*" % fechahora[0:fechahora.index(" / ")])
		return fechahora[0:fechahora.index(" / ")]

	def getTime(self, fechahora):
		#print("*%s*" % fechahora[fechahora.index(" / ")+3:])
		return fechahora[fechahora.index(" / ")+3:]

	def isPrimerHitoDelDia(self, h):

		for hito in self.hitos:
			day_hito = self.getDate(hito.fechahora)
			day_h = self.getDate(h.fechahora)
			if day_hito == day_h:
				if h.inicio < hito.inicio:
					return True
				else:
					return False

		return True

	def isUltimoHitoDelDia(self, h):

		for hito in self.hitos:
			day_hito = self.getDate(hito.fechahora)
			day_h = self.getDate(h.fechahora)
			if day_hito == day_h:
				if h.inicio > hito.inicio:
					return True
				else:
					return False
		return True

	def validbetween(self, hito, inicial, final):

		if inicial is None:
			if ((hito.inicio + hito.tema.duracion + self.distanciabetween(hito, final)) < final.inicio):
				return True
		elif final is None:
			if (hito.inicio > (inicial.inicio + inicial.tema.duracion+self.distanciabetween(hito, inicial))):
				return True
		else:
			if ((hito.inicio + hito.tema.duracion + self.distanciabetween(hito, final)) < final.inicio) and \
				(hito.inicio > (inicial.inicio + inicial.tema.duracion + self.distanciabetween(inicial, hito))):
				return True

		return False

	def distanciabetween(self, origen, destino):
		return self.distancias.between(origen.ubicacion, destino.ubicacion)

	def report(self):

		print("")
		print("Combinación (%d) %d" % (self.id, self.numero))
		print("")

		self.hitos.report()
		print()

	def get_html(self, max=None):
		return self.hitos.get_htmltable()
