# -*- coding: utf-8 -*-
# Copyright (c) 20014 Patricio Moracho <pmoracho@gmail.com>
#
# Bafici.Resolver.Gui.py
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

"""
TO DO:
	+ Output
	+ Agregar info del film
	+ Edición de las tablas del sistema
	+ Bug al eliminar Seleccionados
"""
try:
	import sys
	from PyQt4 import QtCore
	from PyQt4 import QtGui
	from PyQt4.QtCore import QAbstractListModel
	from PyQt4.QtCore import QAbstractTableModel
	from PyQt4.QtCore import QModelIndex
	from PyQt4.QtCore import SIGNAL
	from PyQt4.QtGui import QDialog

	from Engine import Engine
	from MainWindow import Ui_MainWindow

except ImportError as err:
	modulename = err.args[0].partition("'")[-1].rpartition("'")[0]
	print("\nError: No fue posible importar el modulo: %s" % modulename)
	sys.exit(-1)


__author__ 		= "Patricio Moracho <pmoracho@gmail.com>"
__appname__ 	= "baficiresolver"
__appdesc__ 	= "Generador de combinaciones de películas para el festival de cine independiente (BAFICI)"
__license__ 	= 'GPL v3'
__copyright__ 	= "2014, %s" % (__author__)
__version__ 	= "1.1"
__date__ 		= "2014/06/24 13:42:03"


class MainWindowClass(QtGui.QDialog, Ui_MainWindow):

	def __init__(self, parent=None):

		QDialog.__init__(self, parent)

		self.Engine = Engine()
		self.Engine.register(self)
		"""
		temas = "656,1240,525,656,1240,525,142,1263,1031,154,1134,426,531,884,74,759,621,756,995,648,315,1146,538,1028,70,390,33,59,819,453,1046,180,880"
		for codigotema in temas.split(","):
			self.Engine.addTemaSeleccion(codigotema)
		"""
		self.setupUi(self)
		self.postsetupUi()

	def update(self, *args, **kwargs):
		# print("args: {0}\nkwargs: {1}".format(args, kwargs))
		msg = "{0}".format(args[0])
		self.statusLabel.setText(msg)
		QtGui.QApplication.processEvents()

	def salirBtn_clicked(self):
		QtCore.QCoreApplication.instance().quit()

	def postsetupUi(self):

		self.label.setTextFormat(1)
		self.label.setText("Selecciones los contenidos que desea ver. Busque las peliculas ingresando parte del texto o buscandola en la lista.<br/>Agregue cada pelicula a la selección y por último, haciendo click en el botón <b>\"Combinar\"</b> se generarán las combinaciones posibles.")

		self.temasModel = TemasModel(self.Engine.Temas, self)
		self.temasList.setModel(self.temasModel)
		self.temasList.doubleClicked.connect(self.selitem)

		self.temasSeleccionadosModel = TemasModel(self.Engine.TemasSeleccion, self)
		self.temasSeleccionadosList.setModel(self.temasSeleccionadosModel)
		self.temasSeleccionadosList.doubleClicked.connect(self.removeitem)

		self.algoritmoCombo.addItems(self.Engine.getAlgoritmosHabilitados())
		index = self.algoritmoCombo.findText(self.Engine.algoritmoDefault, QtCore.Qt.MatchFixedString)
		if index >= 0:
			self.algoritmoCombo.setCurrentIndex(index)

		self.loadTables()
		self.tablasCheck_clicked()

		self.tabWidget.removeTab(self.tabWidget.indexOf(self.outputTab))

		# connections
		self.connect(self.temaEdit, SIGNAL("textChanged(QString)"), self.text_changed)
		self.salirBtn.clicked.connect(self.salirBtn_clicked)
		self.combinarBtn.clicked.connect(self.combinar)
		self.printBtn.clicked.connect(self.textPreview)
		self.desdeCheck.clicked.connect(self.desdeCheck_clicked)
		self.hastaCheck.clicked.connect(self.hastaCheck_clicked)
		self.tablasCheck.clicked.connect(self.tablasCheck_clicked)

		self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMinMaxButtonsHint)

		self.statusSeleccionados()
		self.temaEdit.setFocus()
		self.setWindowTitle(__appname__)
		self.resize(800, 600)

	def desdeCheck_clicked(self):
		self.desdeTime.setEnabled(self.desdeCheck.isChecked())

	def hastaCheck_clicked(self):
		self.hastaTime.setEnabled(self.hastaCheck.isChecked())

	def tablasCheck_clicked(self):

		if self.tablasCheck.isChecked():
			self.tabWidget.addTab(self.ubicacionesTab 	, "Ubicaciones")
			self.tabWidget.addTab(self.peliculasTab		, "Peliculas")
			self.tabWidget.addTab(self.distanciasTab 	, "Distancias")
			self.tabWidget.addTab(self.proyecionesTab 	, "Proyecciones")
		else:
			self.tabWidget.removeTab(self.tabWidget.indexOf(self.ubicacionesTab))
			self.tabWidget.removeTab(self.tabWidget.indexOf(self.peliculasTab))
			self.tabWidget.removeTab(self.tabWidget.indexOf(self.distanciasTab))
			self.tabWidget.removeTab(self.tabWidget.indexOf(self.proyecionesTab))

	def loadTables(self):

		UbicacionesCols = [
					("#Interno"				, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight	, "codigo"),
					("Sala"					, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft	, "nombre"),
					("Barrio"				, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft	, "barrio"),
				]

		TemasCols = [
					("#Interno"				, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight	, "codigo"),
					("Nombre"				, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft	, "nombre"),
					("Duracion"				, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight	, "duracion"),
					("Información adicional", QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft	, "info"),
				]

		DistanciasCols = [
					("Origen"				, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft	, "origen"),
					("Destino"				, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft	, "destino"),
					("Distancia (min.)"		, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight	, "distancia"),
				]

		ProyeccionesCols = [
					("Tema"					, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft	, "tema"),
					("Ubicacion"			, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft	, "ubicacion"),
					("Inicio (min)"			, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight	, "inicio"),
					("Fecha/Hora"			, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight	, "fechahora"),
				]

		self.loadTableData(self.ubicacionesTable, self.Engine.Ubicaciones, UbicacionesCols)
		self.loadTableData(self.temasTable, self.Engine.Temas, TemasCols)
		self.loadTableData(self.distanciasTable, self.Engine.Distancias, DistanciasCols)
		self.loadTableData(self.proyeccionesTable, self.Engine.Hitos, ProyeccionesCols)

	def loadTableData(self, tableobj, dataobj, columnas):

		tableobj.setRowCount(len(dataobj))
		tableobj.setColumnCount(len(columnas))
		tableobj.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)

		header = [titulo for (titulo, align, atributo) in columnas]
		tableobj.setHorizontalHeaderLabels(header)

		for col, (titulo, align, atributo) in enumerate(columnas):
			tableobj.horizontalHeaderItem(col).setTextAlignment(align)

		for row, objeto in enumerate(dataobj):
			if row % 2 == 0:
				color = QtGui.QColor(243, 244, 255)
			else:
				color = QtGui.QColor(202, 212, 255)

			for col, (titulo, align, atributo) in enumerate(columnas):
				item = QtGui.QTableWidgetItem(str(getattr(objeto, atributo)))
				item.setTextAlignment(align)
				item.setBackground(color)
				tableobj.setItem(row, col, item)

			tableobj.setRowHeight(row, 20)

		tableobj.resizeColumnsToContents()
		tableobj.show()

	def combinar(self):

		if len(self.Engine.TemasSeleccion) > 0:
			self.Engine.setfilter("horadesde", "")
			self.Engine.setfilter("horahasta", "")
			if self.desdeTime.isEnabled():
				self.Engine.setfilter("horadesde", self.desdeTime.text())
			if self.hastaTime.isEnabled():
				self.Engine.setfilter("horahasta", self.hastaTime.text())

			algoritmo = self.algoritmoCombo.currentText()
			self.Engine.Combinaciones.clear()

			try:
				self.Engine.generar_combinaciones(algoritmo)
				s = """
					<style type="text/css">
						h1{font-size:16px;font-family:Verdana, Geneva, sans-serif;}
						h2{font-size:14px;font-family:Verdana, Geneva, sans-serif;}
						h3{font-size:12px;font-family:Verdana, Geneva, sans-serif;}
						.cls_table  {border-width:1px;border-style:solid;border-color:#004f6f;margin-top: 0px;margin-bottom: 0px;font-family:Verdana, Geneva, sans-serif;font-size:12px;}
						.cls_table td{padding:3px 5px;overflow:hidden;word-break:normal;color:#444;background-color:#F7FDFA;border-width:1px;border-style:solid;border-color:#004f6f}
						.cls_table th{padding:3px 5px;overflow:hidden;word-break:normal;color:#fff;background-color:#26ADE4;border-width:1px;border-style:solid;border-color:#004f6f}
						.cls_table .cls_header{font-weight:bold;background-color:#004f6f;}
						.cls_table .cls_row1{background-color:#D2E4FC;}
						.cls_table .cls_row2{background-color:#F7FDFA;}
						.cls_table .cls_totales_1 {background-color:#D2E4FC;font-weight:bold;}
						.cls_table .cls_totales_2 {background-color:#F7FDFA;font-weight:bold;}
						.cls_table .cls_copyright_1 {background-color:#D2E4FC;font-weight:bold;font-size:8px;font-family:Verdana, Geneva, sans-serif;}
						.cls_table .cls_copyright_2 {background-color:#F7FDFA;font-weight:bold;font-size:8px;font-family:Verdana, Geneva, sans-serif;}
					</style>
				"""
				if len(self.Engine.TemasSeleccion) == self.Engine.Combinaciones.getbestcount():
					s = s + "<h1>Exito! se ha conseguido programar todas <br/>las películas propuestas</h1>"
				else:
					s = s + "<h1>Lo siento, del total de películas seleccionadas (%d) <br/>se han conseguido programar %d</h1>" % (len(self.Engine.TemasSeleccion), self.Engine.Combinaciones.getbestcount())

				s = s + self.Engine.Combinaciones.filterbest().get_html()

				self.tabWidget.addTab(self.outputTab 	, "Resultado")

				self.webView.setHtml(s)
				self.tabWidget.setCurrentIndex(self.tabWidget.indexOf(self.outputTab))
				self.webView.setFocus()

			except Exception as e:
				QtGui.QMessageBox.information(self, __appname__, str(e))
		else:
			QtGui.QMessageBox.information(self, __appname__, "Debe seleccionar al menos una película")

	def selitem(self, index):
		"""
		Selecciona un tema pelicula
		"""
		t = self.temasModel.tema(index)
		self.Engine.addTemaSeleccion(t.codigo)
		self.temasSeleccionadosList.reset()
		self.statusSeleccionados()
		self.temaEdit.setText("")
		self.temaEdit.setFocus()

	def removeitem(self, index):
		"""
		Remueve un Tema/Pelicula de la selección
		"""
		t = self.temasSeleccionadosModel.tema(index)
		if t in self.Engine.TemasSeleccion:
			self.Engine.TemasSeleccion.remove(t)
			self.temasSeleccionadosList.reset()

		self.statusSeleccionados()

	def statusSeleccionados(self):
		if len(self.Engine.TemasSeleccion) == 0:
			self.statusSelText.setText("No se han seleccionado películas")
		else:
			self.statusSelText.setText("Seleccionados: %d de %d" % (len(self.Engine.TemasSeleccion), len(self.Engine.Temas)))

	def text_changed(self):
		"""
		updates the list of possible completions each time a key is pressed
		"""
		pattern = str(self.temaEdit.text())
		self.new_list = [item for item in self.Engine.Temas if item.nombre.lower().find(pattern.lower()) == 0]
		self.temasModel.setAllData(self.new_list)

	def tab_pressed(self):
		"""
		completes the word to the longest matching string when the tab key is pressed
		"""
		# only one item in the completion list
		if len(self.new_list) == 1:
			newtext = self.new_list[0].nombre + " "
			self.temaEdit.setText(newtext)
		# more than one remaining matches
		elif len(self.new_list) > 1:
			match = self.new_list.pop(0).nombre
			for word in self.new_list:
				match = string_intersect(word.nombre, match)
			self.temaEdit.setText(match)

	def textPrint(self):
		dialog = QtGui.QPrintDialog()
		if dialog.exec_() == QtGui.QDialog.Accepted:
			# self.salidaText.document().print_(dialog.printer())
			self.webView.document().print_(dialog.printer())

	def textPreview(self):
		dialog = QtGui.QPrintPreviewDialog()
		# dialog.paintRequested.connect(self.salidaText.print_)
		dialog.paintRequested.connect(self.webView.print_)
		dialog.exec_()

	def keyPressEvent(self, e):

		if e.key() == QtCore.Qt.Key_Escape:
			self.close()

	def closeEvent(self, event):

		reply = QtGui.QMessageBox.question(self, __appname__,
				"Desea salir?", QtGui.QMessageBox.Yes |
				QtGui.QMessageBox.No, QtGui.QMessageBox.No)

		if reply == QtGui.QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()


def string_intersect(str1, str2):
	newlist = []
	for i, j in zip(str1, str2):
		if i == j:
			newlist.append(i)
		else:
			break
	return ''.join(newlist)


class TemasModel(QAbstractListModel):

	def __init__(self, datain, parent=None, *args):
		"""
		datain: a list where each item is a row
		"""
		QAbstractTableModel.__init__(self, parent, *args)
		self.listdata = datain

	def rowCount(self, parent=QModelIndex()):
		return len(self.listdata)

	def tema(self, index):
		if index.isValid():
			return self.listdata[index.row()]
		else:
			return None

	def data(self, index, role):
		# print(index.row())
		if index.isValid() and role == QtCore.Qt.DisplayRole and index.row() < len(self.listdata):
			t = self.listdata[index.row()]
			return t.nombre
		else:
			return None

	def setAllData(self, newdata):
		"""
		replace all data with new data
		"""
		self.listdata = newdata
		self.reset()


def main():

		app = QtGui.QApplication(sys.argv)

		style = 'Cleanlooks'
		app.setStyle(QtGui.QStyleFactory.create(style))
		app.setPalette(QtGui.QApplication.style().standardPalette())

		app.setWindowIcon(QtGui.QIcon('res/app.png'))

		locale = QtCore.QLocale.system().name()
		translator = QtCore.QTranslator()
		if getattr(sys, 'frozen', False):
			reptrad = "translations"
		else:
			reptrad = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)
			translator.load("qt_" + locale, reptrad)
			app.installTranslator(translator)

		myWindow = MainWindowClass(None)
		myWindow.show()

		# print(_('This is a translatable string.'))
		sys.exit(app.exec_())


if __name__ == "__main__":

	try:
		main()
	except Exception as e:
		QtGui.QMessageBox.information(None, __appname__, str(e))
