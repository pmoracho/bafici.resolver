# -*- coding: utf-8 -*-
# Copyright (c) 20014 Patricio Moracho <pmoracho@gmail.com>
#
# Distancias.py
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

__author__ 	= "Patricio Moracho (pmoracho@gmail.com)"
__version__ = "1.1"
__date__ 	= "2014/06/24 13:42:03"
__magic__ 	= "menos las luz del sol"

from Object import Object

#################################################################################################################################################
## Distancias
#################################################################################################################################################


class Distancias(Object):

	"""
	Clase para el manejo de una colección de Distancias entre ubicaciones
	"""

	def __init__(self):

		Object.__init__(self)
		self._items = []

	def __get_nice_string(list):
		return "[" + ", ".join(str(item) for item in list) + "]"

	def __str__(self):
		"""String representation"""
		return '[%s: (%d), %s]' % (self.__class__.__name__, self.id, Distancias.__get_nice_string(self._items))

	def __iter__(self):
		return iter(self._items)

	def __getitem__(self, index):
		"""Get an item"""
		return self._items[index]

	def __delitem__(self, key):
		"""Delete an item"""
		del self._items[key]

	def __len__(self):
		"""Len of the list container"""
		return len(self._items)

	def __contains__(self, item):
		return item in self._items

	def add(self, object):
		"""Add an item to list"""
		self._items.append(object)

	def remove(self, key):
		"""Delete an item"""
		self.__delitem__(key)

	def report(self):

		rec = 0

		format = "| %5s | %-30s | %-30s | %10s |"
		header = "| %5s | %-30s | %-30s | %10s |" % ("Id", "Origen", "Destino", "Distancia")

		print("")
		print("Distancias: (%d)" % (self.id))
		print("-" * len(header))
		print(header)
		print("-" * len(header))

		for item in self._items:
			rec = rec+1
			print(format % (item.id, item.origen.nombre, item.destino.nombre, item.distancia))

		print("-" * len(header))
		print("Total de registros: %d" % rec)
		print()

	def csv(self):
		"""
		Salida tipo csv
		"""
		format = "%s;%s;%s;%s;%s"
		header = format % ("Origen", "Destino", "Distancia", "Barrio Origen", "Barrio Destino")
		print(header)
		for item in self._items:
			print(format % (item.origen.codigo, item.destino.codigo, item.distancia, item.origen.barrio, item.destino.barrio))

	def between(self, origen, destino):
		"""
		Retorna la distancia entre dos ubicaciones
		"""
		if origen == destino:
			return 1

		for item in self._items:
			if item.origen == origen and item.destino == destino:
				return item.distancia
			if item.origen == destino and item.destino == origen:
				return item.distancia

		return 0
