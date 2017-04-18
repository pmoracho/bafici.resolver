
#!/usr/bin/python
# -*- coding: utf-8 -*-

from cx_Freeze import setup, Executable

import sys
import os.path
import shutil

# Remove the existing folders folder
shutil.rmtree("build", ignore_errors=True)
shutil.rmtree("dist", ignore_errors=True)


includefiles 	= ["data", "res"]
includes 		= []
excludes 		= ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
					'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
					'Tkconstants', 'Tkinter']
packages 		= []
path 			= []


def read(*paths):
	""" read files """
	with open(os.path.join(*paths), 'r') as filename:
		return filename.read()


if sys.platform == 'win32':
	executables = [
		Executable(	script="Bafici.Resolver.Gui.py",
					initScript=None,
					base='Win32GUI',
					targetName="Bafici.Resolver.Gui.exe",
					compress=True,
					copyDependentFiles=True,
					appendScriptToExe=False,
					appendScriptToLibrary=False,
					icon=os.path.join("res", "app.ico")
					)
				]
else:
	executables = [
		Executable(	script="Bafici.Resolver.Gui.py",
					initScript=None,
					targetName="Bafici.Resolver.Gui",
					copyDependentFiles=True,
					icon=os.path.join("res", "app.ico")
					)
				]

setup(	name="Bafici.Resolver",
		version='1.0',
		description='Generador de combinaciones de peliculas para el festival de cine independiente (BAFICI)',
		author="Patricio Moracho",
		#long_description=(read('README.rst')),
		license='GPL v3',
		author_email="pmoracho@gmail.com",
		url="https://bitbucket.org/pmoracho/python.projects",
		packages=packages,
		classifiers=[
			'Programming Language :: Python :: 3.3',
		],

		#options = dict(build_exe = buildOptions),
		options = {"build_exe": {	"includes": includes,
									"excludes": excludes,
									"path": path,
									"include_msvcr": True,
									"include_files": includefiles
								}
				},
		executables = executables
	)
