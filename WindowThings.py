#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore
#from WidgetThings import *

class Window(QtGui.QMainWindow):
	
	def __init__(self):
		super(Window, self).__init__()
		self.setGeometry(800, 50, 500, 300)
		self.setWindowTitle('DaThings')
		self.setWindowIcon(QtGui.QIcon('dt.png'))
		# window always on top
		#self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		# frameless window
		#self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		#self.setWindowFlags(QtCore.Qt.WindowShadeButtonHint)
		
		
		# List of things
		self.listOfThings = []
		self.filename = 'DaThings.txt'
		# Widget of things, parent = self
		self.treeWidget = QtGui.QListWidget(self)
		self.treeWidget.setGeometry(QtCore.QRect(0, 40, 200, 200))
		# Load list of things from file and add items to widget
		self.make_tree()
		
		# 3 main function of app ( quit, add, delete )
		quitAction = QtGui.QAction('Quit!', self)
		quitAction.setShortcut('Esc')
		quitAction.setStatusTip('Exit')
		quitAction.triggered.connect(sys.exit)
		
		addThing = QtGui.QAction('Add thing!', self)
		addThing.setShortcut('Ctrl+E')
		addThing.setStatusTip('Add thing')
		addThing.triggered.connect(self.add_thing)
		
		deleteThing = QtGui.QAction('Delete thing!', self)
		deleteThing.setShortcut('Del')
		deleteThing.setStatusTip('Just delete')
		deleteThing.triggered.connect(self.delete_thing)
		
		self.statusBar()
		mainMenu = self.menuBar()
		fileMenu = mainMenu.addMenu('&File')
		fileMenu.addAction(addThing)
		fileMenu.addAction(deleteThing)
		fileMenu.addAction(quitAction)
		
		self.home()
		
	def home(self):
		# show 2 buttons, list of things and main window
		addButton = QtGui.QPushButton('Add (Ctrl+E)', self)
		addButton.clicked.connect(self.add_thing)
		addButton.resize(170, 80)
		addButton.move(300, 50)
		
		deleteButton = QtGui.QPushButton('Delete thing (Del)', self)
		deleteButton.clicked.connect(self.delete_thing)
		deleteButton.resize(170, 80)
		deleteButton.move(300, 150)
		
		self.treeWidget.show()
		self.show()
		
	def delete_thing(self):
		pass
		
	def add_thing(self):
		self.addWidget = QtGui.QWidget()
		# setGeometry(x, y, widht, height)
		self.addWidget.setGeometry(250, 150, 300, 200)		
		
		textEdit = QtGui.QLineEdit(self.addWidget)
		textEdit.resize(300, 40)
		
		# here it should be checkbox  example ---> [x] important!
		# ( ... )
		checkBox = QtGui.QCheckBox('Important', self.addWidget)
		checkBox.move(30, 150)
		#checkBox.toggle()
		
		# invisible buttons
		exitButton = QtGui.QPushButton('Back', self.addWidget)
		exitButton.clicked.connect(self.addWidget.close)
		exitButton.setShortcut('Esc')
		exitButton.resize(0,0)
		
		saveButton = QtGui.QPushButton('Save', self.addWidget)
		saveButton.clicked.connect(self.save_thing)
		saveButton.setShortcut('Return')
		saveButton.resize(0,0)
		
		importantButton = QtGui.QPushButton('Make important', self.addWidget)
		importantButton.clicked.connect(self.make_important)
		importantButton.setShortcut('Ctrl+I')
		importantButton.resize(0,0)
		
		self.addWidget.show()
		
	def save_thing(self):
		try:
			text = self.addWidget.findChild(QtGui.QLineEdit).text()
			text += '\n'
			file = open(self.filename, 'a')

			file.write(text)
			file.close()
			self.make_tree()

			self.addWidget.findChild(QtGui.QLineEdit).clear()
		
		except AttributeError:
			print ('ERROR: Niepowodzenie zapisu.')
		
	def make_important(self):
		self.addWidget.findChild(QtGui.QCheckBox).toggle()
		
	def load_list(self):
		thing = ''
		
		try:
			file = open(self.filename, 'r')
			with file:
				text = file.read()
				thing += text

			self.listOfThings = thing.split('\n')
			file.close()
		except IOError:
			# create new file if filename doesn't exist
			file = open(self.filename, 'a')
			file.close()	
		
	def make_tree(self):
		self.load_list()
		self.treeWidget.clear()
		for thing in self.listOfThings:
			self.treeWidget.addItem(thing)
			#self.treeWidget.item(0).setBackgroundColor(QtGui.QColor(100,50,200))
			
		
	def delete_thing(self):
		#self.tree.itemClicked.connect(self.tree.on_treeView_clicked)
		#print [str(x.text()) for x in self.treeWidget.selectedItems()]
		selected = self.treeWidget.selectedItems()
		
		# delete thing from tree
		if selected != []:
			selected = selected[0]
			self.treeWidget.takeItem(self.treeWidget.row(selected))
		
		# delete from listOfThings
		self.listOfThings.remove(str(selected.text()))
		
		# delete from file
		file = open(self.filename, 'r+')
		lines = file.readlines()
		file.seek(0)
		for l in lines:
			if l != str(selected.text()+'\n'):
				file.write(l)
		file.truncate()
		file.close()
		
		
		
		
def run():
	app = QtGui.QApplication(sys.argv)
	GUI = Window()
	sys.exit(app.exec_())
	
run()