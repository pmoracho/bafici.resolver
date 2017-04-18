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

__author__ 		= "Patricio Moracho <pmoracho@gmail.com>"
__appname__		= "baficiresolver"
__appdesc__		= "Generador de combinaciones de películas para el festival de cine independiente (BAFICI)"
__license__   	= 'GPL v3'
__copyright__ 	= "2014, %s" % (__author__)
__version__ 	= "1.1"
__date__ 		= "2014/06/24 13:42:03"
__magic__ 		= ""

import sys
import gettext

##################################################################################################################################################
## Traducir algunas cadenas de argparse
##################################################################################################################################################


def my_gettext(s):

	current_dict = {'usage: ': 'uso: ',
					'optional arguments': 'argumentos opcionales',
					'show this help message and exit': 'mostrar esta ayuda y salir',
					'positional arguments': 'argumentos posicionales'}

	if s in current_dict:
		return current_dict[s]
	return s

gettext.gettext = my_gettext

import argparse

from Engine import Engine

"""
**positional arguments**
**optional arguments**
**show this help message and exit**
**usage: **
**usage: **
"""


##################################################################################################################################################
## Inicializar parametros del programa
##################################################################################################################################################
def init_argparse():

	cmdparser = argparse.ArgumentParser(prog=__appname__,
										description="%s\n%s\n" % (__appdesc__, __copyright__),
										epilog="",
										formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=27)
										)

	cmdparser.add_argument("--version"		, action='version', version=__version__)
	cmdparser.add_argument('--debug'		, action='store_true',  help='Print debug information')
	cmdparser.add_argument('--seleccion'	, type=str, dest="seleccion", help="Selección de las peliculas a combinar, por código, por ej. 123,45,67", metavar="\"peliculas\"")
	cmdparser.add_argument('--search'		, type=str, action="store", dest="search", help="Buscar un determinado film por título", metavar="\"texto\"")
	cmdparser.add_argument('--horadesde'	, type=str, dest="horadesde", help="Hora a partir de la cual se quiere comenzar el evento. Por ej. 17:00", metavar="\"hora\"")
	cmdparser.add_argument('--horahasta'	, type=str, dest="horahasta", help="Hora hasta dónde se quiere participar del evento. Por ej. 23:00", metavar="\"hora\"")
	cmdparser.add_argument('--algoritmo'	, type=str, action="store", dest="algoritmo", help="Algoritmo a utilizar (default=MT1)", metavar="MT1 o MT2", default="MT1")
	cmdparser.add_argument('--intentos'		, type=int, action="store", dest="intentos", help="Cantidad de intentos (Solo válido para algunos algoritmos, default=100)", metavar="cantidad", default=1)

	return cmdparser


def showerror(msg):
	print("\n!!!! %s error: %s\n" % (__appname__, msg))

#################################################################################################################################################
## Main program
#################################################################################################################################################
if __name__ == "__main__":

	cmdparser = init_argparse()
	args = cmdparser.parse_args()
	e = Engine()

	if not args.search and not args.seleccion:
		cmdparser.print_help()
		sys.exit()

	# Search items ##############################################################################################################################
	if args.search:
		e.Temas.filterbynombre(args.search).report()
		sys.exit()

	if args.horadesde:
		e.setfilter("horadesde", args.horadesde)

	if args.horahasta:
		e.setfilter("horahasta", args.horahasta)

	# Process selection ########################################################################################################################
	if args.seleccion:
		for codigotema in args.seleccion.split(","):
			e.addTemaSeleccion(codigotema)

		if args.algoritmo == "MT0":
			e.generarCombinaciones_MT0()
		elif args.algoritmo == "MT1":
			e.generarCombinaciones_MT1(int(args.intentos))
		elif args.algoritmo == "MT2":
			e.generarCombinaciones_MT2(int(args.intentos))
		elif args.algoritmo == "MT3":
			e.generarCombinaciones_MT3(int(args.intentos))
		elif args.algoritmo == "MT4":
			e.generarCombinaciones_MT4()
		elif args.algoritmo == "MT5":
			e.generarCombinaciones_MT5()
		elif args.algoritmo == "MT6":
			e.generarCombinaciones_MT6()
		else:
			showerror("Se debe establecer una algoritmo válido")
			cmdparser.print_usage()
			sys.exit()
		"""
		elif args.algoritmo == "MT7":
			e.generarCombinaciones_MT7(int(args.intentos))
		"""

		#e.TemasSeleccion.report()

		e.Combinaciones.filterbest().report(10)

		#e.HitosSeleccion().report()

		if len(e.TemasSeleccion) == e.Combinaciones.getbestcount():
			print("Exito! se ha conseguido programar todas las películas propuestas")
		else:
			print("Lo siento, del total de películas seleccionadas (%d) se han conseguido programar %d" % (len(e.TemasSeleccion), e.Combinaciones.getbestcount()))

	else:
		showerror("Se debe establecer una selección de peliculas")
		cmdparser.print_usage()
		sys.exit(0)

	sys.exit(0)
