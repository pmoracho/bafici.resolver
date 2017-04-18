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

import subprocess

python_bin = "d:\pm\bin\Python34\python.exe"


def bin():

	cmd = "%s ./setup.py build" % python_bin
	cmd = "py ./setup.py build"

	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	out, err = p.communicate()
	for lin in out:
		print(lin)
	"""
	result = out.split('\n')
	"""

def Main():
	bin()
	pass

#################################################################################################################################################
## Main program
#################################################################################################################################################
if __name__ == "__main__":
	Main()
