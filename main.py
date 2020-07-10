import sys
import MySQLdb as mdb
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QTableWidgetItem, \
	QDialog, QLineEdit, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
import wishlist


DB = 'wishlist'
TABLES = dict()
TABLES['notes'] = (
	"""CREATE TABLE `notes` (`id` int(11) NOT NULL AUTO_INCREMENT,
	`name` varchar(50) NOT NULL UNIQUE,
	`price` integer NOT NULL,
	`link` varchar(255) NOT NULL,
	`comment` varchar(255) NOT NULL,
	PRIMARY KEY (`id`))""")

con = mdb.connect(user='sammy', password='jhYh76&7')
cursor = con.cursor()


def create_db():
	print("Creating database")
	try:
		cursor.execute(
			"CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB))
	except mdb.Error as e:
		print("Failed creating database: {}".format(e))
		exit(1)


def add_note(name, price, link, comment=""):
	sql = """INSERT INTO notes
				(name, price, link, comment)
				VALUES (%s, %s, %s, %s)"""
	args = (name, price, link, comment)
	cursor.execute(sql, args)
	con.commit()


def update_note(name, price, link, comment, name_old):
	sql = """UPDATE notes
				SET name=%s, price=%s, link=%s, comment=%s
				WHERE name=%s"""
	args = (name, price, link, comment, name_old)
	cursor.execute(sql, args)
	con.commit()


def delete_note(name):
	sql = "DELETE FROM notes WHERE name = %s"
	cursor.execute(sql, (name, ))
	con.commit()


def get_all():
	query = "SELECT name, price, link, comment FROM notes"
	cursor.execute(query)
	res = []
	for (name, price, link, comment) in cursor:
		res.append([name, str(price), link, comment])
	return res


class Form(QDialog):
	def __init__(self, parent=None):
		super(Form, self).__init__(parent)

		self.only_int = QIntValidator()
		self.label_name = QLabel("Name:")
		self.name = QLineEdit()

		self.label_price = QLabel("Price:")
		self.price = QLineEdit()
		self.price.setValidator(self.only_int)

		self.label_link = QLabel("Link:")
		self.link = QLineEdit()

		self.label_comment = QLabel("Comment:")
		self.comment = QLineEdit()

		self.button = QPushButton("Create")
		layout = QVBoxLayout()
		layout.addWidget(self.label_name)
		layout.addWidget(self.name)
		layout.addWidget(self.label_price)
		layout.addWidget(self.price)
		layout.addWidget(self.label_link)
		layout.addWidget(self.link)
		layout.addWidget(self.label_comment)
		layout.addWidget(self.comment)
		layout.addWidget(self.button)
		self.setLayout(layout)
		self.button.clicked.connect(self.add)

	def add(self):
		if self.name.text() != '' and self.price.text() != '' \
				and self.link.text() != '' and self.comment.text() != '':
			self.accept()


class ExampleApp(QtWidgets.QMainWindow, wishlist.Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.btnDelete.clicked.connect(self.delete)
		self.btnAdd.clicked.connect(self.add)
		self.btnEdit.clicked.connect(self.edit)
		self.tableWidget.cellClicked.connect(self.select_row)
		self.table_init()

	def table_init(self):
		header = self.tableWidget.horizontalHeader()
		header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

		wishes = get_all()
		self.tableWidget.setRowCount(len(wishes))
		self.tableWidget.setHorizontalHeaderLabels(["name", "price", "link", "comment"])
		for row, wish in enumerate(wishes):
			for col in range(len(wish)):
				item = QTableWidgetItem()
				item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
				item.setText(wish[col])
				self.tableWidget.setItem(row, col, item)

	def select_row(self):
		self.tableWidget.selectionModel().selectedRows()

	def delete(self):
		items = self.tableWidget.selectedItems()
		data = []
		for i in items:
			data.append(i.text())

		if data:
			index = self.tableWidget.selectionModel().selectedRows()
			for i in index:
				name = i.data()
				delete_note(name)
		self.table_init()

	def add(self):
		dlg = Form(self)
		dlg.setWindowTitle("New note")

		if dlg.exec_():
			name = dlg.name.text()
			price = dlg.price.text()
			link = dlg.link.text()
			comment = dlg.comment.text()

			try:
				add_note(name, price, link, comment)
			except mdb.IntegrityError as e:
				print("Error: {} {} {} ".format(e, type(e), e.args))
				error_dialog = QtWidgets.QErrorMessage(parent=dlg)
				error_dialog.showMessage('Wish name should be unique. Please choose another name')
				error_dialog.exec_()
			self.table_init()

	def edit(self):
		items = self.tableWidget.selectedItems()
		data = []
		for item in items:
			data.append(item.text())

		if data:
			dlg = Form(self)
			dlg.name.setText(data[0])
			dlg.price.setText(data[1])
			dlg.link.setText(data[2])
			dlg.comment.setText(data[3])
			dlg.setWindowTitle("Update your wish!")
			dlg.button.setText("Edit")

			if dlg.exec_():
				name = dlg.name.text()
				price = dlg.price.text()
				link = dlg.link.text()
				comment = dlg.comment.text()
				update_note(name, price, link, comment, data[0])
				self.table_init()


def main():
	try:
		cursor.execute("USE {}".format(DB))
	except mdb.Error as e:
		print("Database {} does not exists.".format(DB))
		if e.args[0] == 1049:
			print("Trying to create database")
			create_db()
			print("Database {} created successfully.".format(DB))
			con.database = DB
		else:
			print(e)
			exit(1)
	for name in TABLES:
		comment = TABLES[name]
		try:
			print("Creating table {}: ".format(name), end='')
			cursor.execute(comment)
		except mdb.Error as e:
			if e.args[0] == 1050:
				print("Already exists.")
			else:
				print(e.args[1])
				exit(1)
		else:
			print("OK")
	app = QtWidgets.QApplication(sys.argv)
	window = ExampleApp()
	window.show()
	app.exec_()
	cursor.close()
	con.close()


if __name__ == '__main__':
	main()
