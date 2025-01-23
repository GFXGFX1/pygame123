import sys
import pygame
import csv
import re
import os
from PyQt6.QtWidgets import QApplication, QDialog, QFormLayout, QLineEdit, QPushButton, QMessageBox

# Определяем цвета
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
purple = (255, 0, 255)
yellow = (255, 255, 0)
gblue = (0, 255, 255)
WALLET_FILE = "wallet.csv"
pygame.init()


class MyApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_dialog = LoginDialog(self)
        self.login_dialog.exec()

    def open_menu_dialog(self, username):
        menu_dialog = MenuDialog(self, username)
        menu_dialog.exec()

    def start_game(self):
        startGame()

    def close_all_windows(self):
        self.login_dialog.close()


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
        self.login_button.clicked.connect(self.check_login)
        layout.addRow(self.login_button)
        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.open_registration_dialog)
        layout.addRow(self.register_button)
        self.setLayout(layout)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if self.username_exists(username):
            if self.validate_login(username, password):
                self.app.close_all_windows()
                self.app.open_menu_dialog(username)
                un = username
                self.accept()
            else:
                QMessageBox.warning(self, "Error", "Invalid username or password.")
        else:
            QMessageBox.warning(self, "Error", "User  does not exist.")

    def username_exists(self, username):
        try:
            if os.path.exists(WALLET_FILE):
                with open(WALLET_FILE, 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row[0] == username:
                            return True
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to check username: {e}")
        return False

    def validate_login(self, username, password):
        try:
            if os.path.exists(WALLET_FILE):
                with open(WALLET_FILE, 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row[0] == username and row[2] == password:
                            return True
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to validate login: {e}")
        return False

    def open_registration_dialog(self):
        registration_dialog = RegistrationDialog(self.app)
        registration_dialog.exec()


class RegistrationDialog(QDialog):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Registration")
        self.setGeometry(100, 100, 400, 400)
        layout = QFormLayout()
        self.username_input = QLineEdit(self)
        layout.addRow("Username:", self.username_input)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow("Password:", self.password_input)
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow("Confirm Password:", self.confirm_password_input)
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.check_registration)
        layout.addRow(self.ok_button)
        self.setLayout(layout)

    def check_registration(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        if not self.validate_username(username):
            QMessageBox.warning(self, "Error",
                                "Username must be between 3 and 15 characters and contain only letters and digits.")
            return
        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return
        if self.username_exists(username):
            QMessageBox.warning(self, "Error", "User  already exists.")
            return
        self.save_user(username, password)
        QMessageBox.information(self, "Success", "Registration successful!")
        self.app.close_all_windows()
        self.app.open_menu_dialog(username)
        self.accept()

    def validate_username(self, username):
        return 3 <= len(username) <= 15 and re.match("^[A-Za-z0-9]+$", username)

    def username_exists(self, username):
        try:
            if os.path.exists(WALLET_FILE):
                with open(WALLET_FILE, 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row[0] == username:
                            return True
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to check username: {e}")
        return False

    def save_user(self, username, password):
        try:
            with open(WALLET_FILE, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([username, 0, password])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save user: {e}")


class MenuDialog(QDialog):
    def __init__(self, app, username):
        global un
        super().__init__()
        self.app = app
        self.username = username
        un = username
        print(un)
        self.setWindowTitle("Menu")
        self.setGeometry(100, 100, 300, 200)
        layout = QFormLayout()
        self.shop_button = QPushButton("Shop")
        self.shop_button.clicked.connect(self.open_shop)
        layout.addRow(self.shop_button)
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.start_game)
        layout.addRow(self.play_button)
        self.setLayout(layout)

    def open_shop(self):
        QMessageBox.information(self, "Shop", "Shop feature not implemented yet.")

    def start_game(self):
        self.app.start_game()


def startGame():
    Trollicon = pygame.image.load('Trollman.png')
    pygame.display.set_icon(Trollicon)

    # Продолжу

    class Wall(pygame.sprite.Sprite):
        def __init__(self, x, y, width, height, color):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface([width, height])
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.rect.top = y
            self.rect.left = x

    def setupRoomOne(all_sprites_list):
        wall_list = pygame.sprite.RenderPlain()
        walls = [[0, 0, 6, 600], [0, 0, 600, 6], [0, 600, 606, 6], [600, 0, 6, 606],
                 [300, 0, 6, 66], [60, 60, 186, 6], [360, 60, 186, 6], [60, 120, 66, 6],
                 [60, 120, 6, 126], [180, 120, 246, 6], [300, 120, 6, 66], [480, 120, 66, 6],
                 [540, 120, 6, 126], [120, 180, 126, 6], [120, 180, 6, 126], [360, 180, 126, 6],
                 [480, 180, 6, 126], [180, 240, 6, 126], [180, 360, 246, 6], [420, 240, 6, 126],
                 [240, 240, 42, 6], [324, 240, 42, 6], [240, 240, 6, 66], [240, 300, 126, 6],
                 [360, 240, 6, 66], [0, 300, 66, 6], [540, 300, 66, 6], [60, 360, 66, 6],
                 [60, 360, 6, 186], [480, 360, 66, 6], [540, 360, 6, 186], [120, 420, 366, 6],
                 [120, 420, 6, 66], [480, 420, 6, 66], [180, 480, 246, 6], [300, 480, 6, 66],
                 [120, 540, 126, 6], [360, 540, 126, 6]]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], blue)
            wall_list.add(wall)
            all_sprites_list.add(wall)

        return wall_list

    class Block(pygame.sprite.Sprite):
        def __init__(self, color, width, height):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface([width, height])
            self.image.fill(white)
            self.image.set_colorkey(white)
            pygame.draw.ellipse(self.image, color, [0, 0, width, height])
            self.rect = self.image.get_rect()

    class Player(pygame.sprite.Sprite):
        change_x = 0
        change_y = 0

        def __init__(self, x, y, filename):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(filename).convert()
            self.rect = self.image.get_rect()
            self.rect.top = y
            self.rect.left = x
            self.prev_x = x
            self.prev_y = y

        def prevdirection(self):
            self.prev_x = self.change_x
            self.prev_y = self.change_y

        def changespeed(self, x, y):
            self.change_x += x
            self.change_y += y

        def update(self, walls, gate):
            old_x = self.rect.left
            new_x = old_x + self.change_x
            prev_x = old_x + self.prev_x
            self.rect.left = new_x

            old_y = self.rect.top
            new_y = old_y + self.change_y
            prev_y = old_y + self.prev_y

            x_collide = pygame.sprite.spritecollide(self, walls, False)
            if x_collide:
                self.rect.left = old_x
            else:
                self.rect.top = new_y
                y_collide = pygame.sprite.spritecollide(self, walls, False)
                if y_collide:
                    self.rect.top = old_y

            if gate != False:
                gate_hit = pygame.sprite.spritecollide(self, gate, False)
                if gate_hit:
                    self.rect.left = old_x
                    self.rect.top = old_y

    class Ghost(Player):
        def changespeed(self, list, ghost, turn, steps, l):
            try:
                z = list[turn][2]
                if steps < z:
                    self.change_x = list[turn][0]
                    self.change_y = list[turn][1]
                    steps += 1
                else:
                    if turn < l:
                        turn += 1
                    elif ghost == "clyde":
                        turn = 2
                    else:
                        turn = 0
                    self.change_x = list[turn][0]
                    self.change_y = list[turn][1]
                    steps = 0
                return [turn, steps]
            except IndexError:
                return [0, 0]

    pygame.init()

    screen = pygame.display.set_mode([606, 606])
    pygame.display.set_caption('Pacman')

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(black)

    clock = pygame.time.Clock()
    pygame.font.init()
    font = pygame.font.Font("freesansbold.ttf", 24)

    w = 303 - 16
    p_h = (7 * 60) + 19
    m_h = (4 * 60) + 19
    b_h = (3 * 60) + 19
    i_w = 303 - 16 - 32
    c_w = 303 + (32 - 16)
    BASE_GHOST_SPEED = 15  # Базовая скорость призраков
    SPEED_INCREMENT = 1
    ghost_speed = BASE_GHOST_SPEED

    # Глобальная переменная для хранения очков после игры
    score2 = 0
    # djn nen ghjljk;b? jr&


if __name__ == "__main__":
    my_app = MyApp()
    sys.exit(my_app.app.exec())
