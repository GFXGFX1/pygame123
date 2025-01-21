import sys
import pygame
import csv
from PyQt6.QtWidgets import QApplication, QDialog, QFormLayout, QLineEdit, QPushButton

# Определяем цвета
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
purple = (255, 0, 255)
yellow = (255, 255, 0)
gblue = (0, 255, 255)
WALLET_FILE = "../wallet.csv"

class MyApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_dialog = LoginDialog(self)
        self.login_dialog.exec()

class LoginDialog(QDialog):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 400)
        layout = QFormLayout()
        self.username_input = QLineEdit(self)
        layout.addRow("Username:", self.username_input)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow("Password:", self.password_input)
        self.login_button = QPushButton("Login")
        layout.addRow(self.login_button)
        self.register_button = QPushButton("Register")
        layout.addRow(self.register_button)
        self.setLayout(layout)

if __name__ == "__main__":
    my_app = MyApp()
    sys.exit(my_app.app.exec())
