import sys
import pygame
import csv
from PyQt6.QtWidgets import QApplication

# Определяем цвета
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
purple = (255, 0, 255)
yellow = (255, 255, 0)
gblue = (0, 255, 255)
WALLET_FILE = "../walli12312et.csv"

class MyApp:
    def __init__(self):
        self.app = QApplication(sys.argv)