# -*- coding: utf-8 -*-
# Copyright (c) 20014 Patricio Moracho <pmoracho@gmail.com>
#
# Hito.py
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
__magic__ 	= "el pasto siempre es mas verde del otro lado"

from Object import Object

#################################################################################################################################################
## Hito
#################################################################################################################################################


class Hito(Object):

	"""
	Clase para el manejo de Hitos / Proyeccciones
	"""

	def __init__(self, tema, ubicacion, inicio, fechahora, fecha=None, hora=None):

		Object.__init__(self)
		self.nro		= 0
		self.tema		= tema
		self.ubicacion	= ubicacion
		self.inicio		= inicio
		self.fechahora	= fechahora
		self.fecha 		= fecha
		self.hora 		= hora
		self.fin		= inicio+tema.duracion

	def __str__(self):
		"""String representation"""
		return '[%s: (%d), %s, %s, %d, %s]' % (self.__class__.__name__, self.id, self.tema, self.ubicacion, self.inicio, self.fechahora)

	def __lt__(self, other):
		return int(self.inicio) < int(other.inicio)

	def __hash__(self):
		return self.nro
