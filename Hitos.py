# -*- coding: utf-8 -*-
  
# Copyright (c) 20014 Patricio Moracho <pmoracho@gmail.com>
#
# Hitos.py
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

from Object 	import Object
from Hito 		import Hito
from random 	import shuffle

#################################################################################################################################################
## Hitos
#################################################################################################################################################
class Hitos(Object):
	"""
	Clase para el manejo de una coleccion de Hitos / Proyecciones
    """
	
	def __init__(self,distancias, horadesde="", horahasta=""):
	
		Object.__init__(self)
		self._items 	= []
		self.position 	= -1
		self.distancias	= distancias
		self.horadesde	= horadesde
		self.horahasta	= horahasta

	def _get_nice_string(list):
		return "[" + ", ".join( str(item) for item in list) + "]"

	def __str__(self):
		"""String representation"""
		return '[%s: (%d), %s]' % (self.__class__.__name__, self.id, Hitos._get_nice_string(self._items))

	def __iter__(self):
		return iter(self._items)

	def __getitem__(self, index):
		"""Get an item"""
		return self._items[index]

	def __setitem__(self, index, item):
		self._items[index] = item

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

	def sort(self):
		self._items.sort()

	def randomize(self):
		hitos = list(self._items)
		shuffle(hitos)
		return hitos
		
	def existtema(self, codigotema):
		for item in self._items:
			if item.tema.codigo == codigotema:
				return True
				
		return False

	def filterbytemas(self, listatemas, filterbytime=False):
		filtered=Hitos(self.distancias)
		for t in listatemas:
			for item in self._items:
				if item.tema.codigo == t.codigo:
					if filterbytime:
						if self.validtimefilter(item):
							filtered.add(item)
					else: 
						filtered.add(item)
				
		return filtered

	def filterbytema(self, codigotema, filterbytime=False):
		filtered=Hitos(self.distancias)
		for item in self._items:
			if item.tema.codigo == codigotema:
				if filterbytime:
					if self.validtimefilter(item):
						filtered.add(item)
				else: 
					filtered.add(item)
				
		return filtered

	def filterbynottema(self, codigotema, filterbytime=False):
		filtered=Hitos(self.distancias)
		for item in self._items:
			if item.tema.codigo != codigotema:
				if filterbytime:
					if self.validtimefilter(item):
						filtered.add(item)
				else: 
					filtered.add(item)
				
		return filtered
		
	def validtimefilter(self,hito):
		"""
		Retorna verdader/falso si el hito entra dentro del desde/hasta hora deseado
		"""
		if self.horadesde == "" and self.horahasta == "":
			return True

		hora = self._items.fechahora[hito.fechahora.index(" / ")+3:]

		hora_hito = datetime.datetime.strptime(hora, "%H:%M")
		
		if self.horadesde != "" :
			hora_desde = datetime.datetime.strptime(self.horadesde, "%H:%M")
			if hora_desde > hora_hito:
				return False

		if self.horahasta != "" :
			hora_hasta = datetime.datetime.strptime(self.horahasta, "%H:%M")
			if hora_hasta < hora_hito:
				return False

		return True

	def report(self):

		rec = 0
		
		format="| %5.5s | %9.9s | %-50.50s | %-30.30s | %8.8s | %8.8s | %8.8s | %15.15s | %8.8s |"
		header=format % ("Nro", "Cod.Tema", "Nombre Tema", "Ubicación", "Duración", "Inicio", "Fin", "Fecha/Hora", "Trayecto")

		print("") 
		print("Hitos: (%d)" % (self.id))
		print("-" * len(header))
		print(header)
		print("-" * len(header))
		
		i=0
		for item in self._items:
			rec=rec+1
			trayecto=0
			if i+1 < len(self._items):
				trayecto = self.distancias.between(item.ubicacion,self._items[i+1].ubicacion)
			i=i+1	
			print(format % ( item.nro, item.tema.codigo, item.tema.nombre, item.ubicacion.nombre, item.tema.duracion, item.inicio, item.fin, item.fechahora, trayecto))
			ant = item

		print("-" * len(header))
		print("Total de registros: %d" % rec)
		print()


	def get_report_text(self):

		rec = 0
		
		salida=""
		format="| %5.5s | %9.9s | %-50.50s | %-30.30s | %8.8s | %8.8s | %8.8s | %15.15s | %8.8s |"
		header=format % ("Nro", "Cod.Tema", "Nombre Tema", "Ubicación", "Duración", "Inicio", "Fin", "Fecha/Hora", "Trayecto")

		salida = salida + "\nHitos:\n"
		salida = salida + ("-" * len(header)) + "\n"
		salida = salida + (header) + "\n"
		salida = salida + ("-" * len(header)) + "\n"
		
		i=0
		for item in self._items:
			rec=rec+1
			trayecto=0
			if i+1 < len(self._items):
				trayecto = self.distancias.between(item.ubicacion,self._items[i+1].ubicacion)
			i=i+1	
			salida = salida + (format % ( item.nro, item.tema.codigo, item.tema.nombre, item.ubicacion.nombre, item.tema.duracion, item.inicio, item.fin, item.fechahora, trayecto))
			salida = salida + "\n"
			ant = item

		salida = salida + ("-" * len(header)) + "\n"
		salida = salida + ("Total de registros: %d\n" % rec)
		salida = salida + ("\n")
		return salida

	def get_htmltable(self):

		html_table_header = """
							<table class="cls_table" cellspacing="0" cellpadding="0">
							  <tr>
							    <th class="cls_header" width="40%"><p align="left">Pelicula</p></th>
							    <th class="cls_header" width="15%"><p align="center">Ubicación</p></th>
							    <th class="cls_header" width="15%"><p align="center">Inicio</p></th>
							    <th class="cls_header" width="15%"><p align="right">Duración (min)</p></th>
							    <th class="cls_header" width="15%"><p align="right">Traslado (min)</p></th>
							  </tr>
							"""
		html_table_row_1 = """
							<tr>
								<td class="cls_row1"><p align="left">[pelicula]</p></td>
								<td class="cls_row1"><p align="center">[ubicacion]</p></td>
								<td class="cls_row1"><p align="center">[fechahora]</p></td>
								<td class="cls_row1"><p align="right">[duracion]</p></td>
								<td class="cls_row1"><p align="right">[traslado]</p></td>
							  </tr>
							"""

		html_table_row_2 = """
							<tr>
								<td class="cls_row2"><p align="left">[pelicula]</p></td>
								<td class="cls_row2"><p align="center">[ubicacion]</p></td>
								<td class="cls_row2"><p align="center">[fechahora]</p></td>
								<td class="cls_row2"><p align="right">[duracion]</p></td>
								<td class="cls_row2"><p align="right">[traslado]</p></td>
							  </tr>
							"""
		html_table_total_1 = """
							<tr>
								<td class="cls_totales_1" align="right" colspan="5">[Totales]</td>
							</tr>
							<tr>
								<td class="cls_copyrigh_1t" align="right" colspan="5">combinación realizada por baficiresolver by pmoracho@gmail.com"</td>
							</tr>
							"""
		html_table_total_2 = """
							<tr>
								<td class="cls_totales_2" align="right" colspan="5">[Totales]</td>
							</tr>
							<tr>
								<td class="cls_copyright_2" align="right" colspan="5">combinación realizada por baficiresolver by pmoracho@gmail.com"</td>
							</tr>
							"""
		html_table_end = '</table>'

		par = False
		
		salida=html_table_header
		rec=0
		i=0
		for item in self._items:
			rec=rec+1
			trayecto=0
			if i+1 < len(self._items):
				trayecto = self.distancias.between(item.ubicacion,self._items[i+1].ubicacion)
			i=i+1	
			if par:
				row = html_table_row_1
				par = False
			else:
				row = html_table_row_2
				par = True

			row = row.replace("[pelicula]",item.tema.nombre)
			row = row.replace("[ubicacion]",item.ubicacion.nombre)
			row = row.replace("[duracion]",("%4d" % item.tema.duracion))
			row = row.replace("[fechahora]",("%s" % item.fechahora))
			row = row.replace("[fin]",("%8d" % item.fin))
			row = row.replace("[traslado]",("%8d" % trayecto))
			salida = salida + row

		if par:
			salida = salida + html_table_total_1.replace("[Totales]",("<h3>Total de registros: %d</h3>" % rec))
		else:
			salida = salida + html_table_total_2.replace("[Totales]",("<h3>Total de registros: %d</h3>" % rec))

		salida = salida + html_table_end
		return salida
