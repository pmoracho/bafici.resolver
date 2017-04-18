# -*- coding: utf-8 -*-
# Copyright (c) 20014 Patricio Moracho <pmoracho@gmail.com>
#
# Temas.py
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
__version__ = "1.0"
__date__ 	= "2014/06/24 13:42:03"
__magic__ 	= "Quién más, quién menos, conoce el juego"

from Object import Object
from random import shuffle

#################################################################################################################################################
## Temas
#################################################################################################################################################


class Temas(Object):

	"""
	Clase para el manejo de una colección de de Temas / Películas.
	"""

	def __init__(self, nombre):

		Object.__init__(self)
		self.nombre	= nombre
		self._items	= []

	def __get_nice_string(list):
		"""Transforma una lista en una represtentación string"""
		return "[" + ", ".join(str(item) for item in list) + "]"

	def __str__(self):
		"""String representation"""
		return '[%s: (%d), %s, %s]' % (self.__class__.__name__, self.id, self.nombre, Temas.__get_nice_string(self._items))

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

	def index(self, item):
		list.index(item)

	def add(self, object):
		"""Add an item to list"""
		self._items.append(object)

	def remove(self, item):
		"""Delete an item"""
		self._items.remove(item)

	def sort(self):
		self.temas.sort()

	def randomize(self):
		temas = list(self._items)
		shuffle(temas)
		return temas

	def report(self):
		"""Reporte de temas"""

		rec = 0

		format = "| %6.6s | %-50.50s | %8.8s | %5.5s |"
		header = format % ("Código", "Nombre", "Duración", "Id")

		print("")
		print("Temas: (%d) %s" % (self.id, self.nombre))
		print("-" * len(header))
		print(header)
		print("-" * len(header))

		for item in self._items:
			rec = rec+1
			print(format % (item.codigo, item.nombre, item.duracion, item.id))

		print("-" * len(header))
		print("Total de registros: %d" % rec)
		print()

	def getbycodigo(self, codigo):
		"""Obtener un tema buscandolo por codigo"""
		for item in self._items:
			if item.codigo == codigo:
				return item
		return None

	def gettemabynombre(self, nombre):
		"""Obtener un tema buscandolo por nombre"""
		for item in self._items:
			if item.nombre == nombre:
				return item

	def filterbynombre(self, nombre):
		"""Obtener una lista auxiliar con valores filtrados por nombre"""
		filtered = Temas("fltrados")
		for item in self._items:
			if item.nombre.lower().find(nombre.lower()) != -1:
				filtered.add(item)
		return filtered
