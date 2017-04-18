# -*- coding: utf-8 -*-
# Copyright (c) 20014 Patricio Moracho <pmoracho@gmail.com>
#
# Tema.py
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

from Object import Object

#################################################################################################################################################
## Tema
#################################################################################################################################################


class Tema(Object):

	"""
	Clase para el manejo de Temas / Peliculas.
	"""

	def __init__(self, codigo, nombre, info, duracion):

		Object.__init__(self)
		self.codigo 	= codigo
		self.nombre 	= nombre
		self.duracion 	= duracion
		self.info 		= info

	def __str__(self):
		"""String representation"""
		#return '[%s: (%d), %s, %s, %s, %d]' % (self.__class__.__name__, self.id, self.codigo, self.nombre, self.info, self.duracion)
		return '[%s, %s, %s, %dmin]' % (self.codigo, self.nombre, self.info, self.duracion)
