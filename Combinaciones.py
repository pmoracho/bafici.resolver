# -*- coding: utf-8 -*-
# Copyright (c) 20014 Patricio Moracho <pmoracho@gmail.com>
#
# Combinaciones.py
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
__magic__ 	= ""

from Object import Object

#################################################################################################################################################
## Combinaciones
#################################################################################################################################################


class Combinaciones(Object):

	"""
	Clase para el manejo de una coleccion de Combinaciones
	"""

	def __init__(self):

		Object.__init__(self)
		self._items = set()

	def _get_nice_string(list):
		return "[" + ", ".join(str(item) for item in list) + "]"

	def __str__(self):
		"""String representation"""
		return '[%s: (%d), %s]' % (self.__class__.__name__, self.id, Combinaciones._get_nice_string(self._items))

	def __iter__(self):
		return iter(self._items)

	def __len__(self):
		"""Len of the list container"""
		return len(self._items)

	def clear(self):
		self._items.clear()

	def add(self, object):
		self._items.add(object)

	def filterbest(self):

		max = self.getbestcount()
		filtered = Combinaciones()
		for item in self._items:
			if len(item) == max:
				filtered.add(item)

		return filtered

	def getbestcount(self):
		return max([len(item) for item in self._items])

	def report(self, max=None):

		for index, item in enumerate(self._items, start=1):
			item.report()
			if max is not None and max == index:
				break

		print("Total de combinaciones posibles: %d" % len(self._items))

	def get_html(self, max=None):

		salida = "</br>"
		salida = salida + ("<h2>Total de combinaciones posibles: %d</h2>" % len(self._items))
		for index, item in enumerate(self._items, start=1):
			salida = salida + ("<h2>Combinación %d</h2>" % (index))
			salida = salida + "<p>"
			salida = salida + item.get_html()
			salida = salida + "</p>"
			if max is not None and max == index:
				break


		return salida
