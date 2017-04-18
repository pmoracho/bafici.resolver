# -*- coding: utf-8 -*-
  
# Copyright (c) 20014 Patricio Moracho <pmoracho@gmail.com>
#
# Ubicaciones.py
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
__magic__ 	= "Hojas muertas que caen"

from Object 	import Object
from Ubicacion 	import Ubicacion

#################################################################################################################################################
## Ubicaciones
#################################################################################################################################################
class Ubicaciones(Object):
	"""
	Clase para el manejo de una coleccion de Ubicaciones
    """
	
	def __init__(self):
	
		Object.__init__(self)
		self._items=[]

	def __str__(self):
		"""String representation"""
		return '[%s: (%d), %s]' % (self.__class__.__name__, self.id, Ubicaciones._get_nice_string(self._items))

	def __iter__(self):
		return iter(self._items)

	def __getitem__(self, index):
		"""Get an item"""
		return self._items[index]
	
	def __delitem__( self, key):
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

	def remove( self, key):
		"""Delete an item"""
		self.__delitem__(key)

	def report(self):
		""" Object reporter """
		rec = 0
		
		format="| %5.5s | %6.6s | %-50.50s |"
		header=format % ("Id", "Código", "Nombre")

		print("") 
		print("Ubicaciones: (%d)" % (self.id))
		print("-" * len(header))
		print(header)
		print("-" * len(header))
		
		for item in self._items:
			rec=rec+1
			print(format % ( item.id, item.codigo, item.nombre))

		print("-" * len(header))
		print("Total de registros: %d" % rec)
		print()
		
	def getbycodigo(self, codigo):
		""" Get an Ubicacion by Codigo """
		for item in self._items:
			if item.codigo == codigo:
				return item
		return None

		
