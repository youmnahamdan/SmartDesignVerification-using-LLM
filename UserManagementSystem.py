from os import name
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QCheckBox, QSizePolicy
)
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, 
    QTableWidgetItem, QMessageBox, QHeaderView, QDialog
)
from PyQt5.QtCore import Qt
import sys

from StyleSheet import *
from Imports import *

   
from PyQt5.QtCore import pyqtSignal

class LoginWidget(QWidget):
    login_successful = pyqtSignal()  # Signal to tell MainWindow that login succeeded

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setMaximumSize(500, 500)

        title_label = QLabel("<h2>Smart Design Verification</h2>")
        title_label.setStyleSheet(f'font-family: "{font_family}"; font-size:22px;')
        subtitle_label = QLabel("Enter your email and password to access your account")

        email_label = QLabel("Email")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")

        password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)

        sign_in_button = QPushButton("Sign In")
        sign_in_button.setFixedWidth(200)
        sign_in_button.clicked.connect(self.on_sign_up)  # connect button

        # Layout
        form_layout = QVBoxLayout()
        form_layout.addStretch()
        form_layout.addWidget(title_label, alignment=Qt.AlignCenter)
        form_layout.addWidget(subtitle_label, alignment=Qt.AlignCenter)
        form_layout.addSpacing(30)
        form_layout.addWidget(email_label)
        form_layout.addWidget(self.email_input)
        form_layout.addSpacing(10)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addSpacing(20)
        form_layout.addWidget(sign_in_button, alignment=Qt.AlignCenter)
        form_layout.addStretch()

        self.setLayout(form_layout)
        self.setStyleSheet(login_style_sheet)

    def on_sign_up(self):
        global db_obj
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            create_msg_box(self, QMessageBox.Critical, "Error", "Please enter both email and password.")  
            return

        user_exists = db_obj.user_exists(email)
        if user_exists:
            correct_password = db_obj.check_password(email, password)
            if correct_password:
                global current_user
                current_user = db_obj.get_user(email)
                self.login_successful.emit()
                
            else:
                create_msg_box(self, QMessageBox.Critical, "Error", "Incorrect password.")  
        else:
            create_msg_box(self, QMessageBox.Critical, "Error", "User not found.")  

class AdminMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QHBoxLayout()
        layout.setSpacing(10)  # Adjust spacing between buttons
        
        # Button Definitions
        self.add_user = self.create_button("Add or Update User")
        self.delete_user = self.create_button("Delete User")

        # Add buttons to layout
        layout.addWidget(self.add_user)
        layout.addWidget(self.delete_user)

        # Set layout
        self.setLayout(setWidgetBG(layout, 'white', -30, 0, -30, 0, border_radius = 5))

    def create_button(self, text, icon_path=None):
        button = QPushButton(text)
        #button.setIcon(QIcon(icon_path))
        button.setStyleSheet(upper_menus_style)
        #button.setIconSize(QSize(32, 32)) 
        return button
  
class UserFormDialog(QDialog):
    def __init__(self, user_data=None):
        super().__init__()
        global db_obj
        self.db_obj = db_obj
        self.user_data = user_data
        self.initUI()

    def initUI(self):
        self.setWindowTitle("User Form")
        layout = QFormLayout()

        self.user_id_input = QLineEdit()
        self.username_input = QLineEdit()
        self.email_input = QLineEdit()
        self.access_level_input = QLineEdit()
        self.password_input = QLineEdit()
        self.rating_input = QLineEdit()

        if self.user_data:
            self.user_id_input.setText(self.user_data[0])
            self.user_id_input.setDisabled(True)
            self.username_input.setText(self.user_data[1])
            self.email_input.setText(self.user_data[2])
            self.access_level_input.setText(self.user_data[3])
            self.password_input.setText(self.user_data[4])
            self.rating_input.setText(self.user_data[5])

        layout.addRow("User ID:", self.user_id_input)
        layout.addRow("Username:", self.username_input)
        layout.addRow("Email:", self.email_input)
        layout.addRow("Access Level:", self.access_level_input)
        layout.addRow("Password:", self.password_input)
        layout.addRow("Rating:", self.rating_input)

        buttons_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_user)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)

        layout.addRow(buttons_layout)
        self.setLayout(layout)

    def save_user(self):
        user_id = self.user_id_input.text().strip()
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        access_level = self.access_level_input.text().strip()
        password = self.password_input.text().strip()
        rating = self.rating_input.text().strip()

        if not all([user_id, email, password]):
            QMessageBox.warning(self, "Warning", "User ID, Email, and Password are required!")
            return

        if self.user_data:
            # Edit user
            self.db_obj.save_or_update_user(user_id, username, email, access_level, password, rating)
        else:
            # Add new user
            self.db_obj.save_or_update_user((user_id, username, email, access_level, password, rating,))

        self.accept()

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class DeleteUserDialog(QDialog):
    def __init__(self):
        super().__init__()
        global db_obj
        self.db_obj = db_obj
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Delete User")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        self.label = QLabel("Enter User ID to delete:")
        self.user_id_input = QLineEdit()
        self.user_id_input.setPlaceholderText("User ID")

        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_user)

        layout.addWidget(self.label)
        layout.addWidget(self.user_id_input)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

    def delete_user(self):
        user_id_text = self.user_id_input.text().strip()
        if not user_id_text.isdigit():
            QMessageBox.critical(self, "Error", "Please enter a valid numeric User ID.")
            return
        
        user_id = int(user_id_text)

        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete user ID {user_id}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            success = self.db_obj.delete_user(user_id)
            if success:
                QMessageBox.information(self, "Success", f"User ID {user_id} deleted successfully.")
                self.accept()  # Close the dialog
            else:
                QMessageBox.critical(self, "Error", "Failed to delete user.")


class AdminDashboard(QWidget):
    def __init__(self):
        super().__init__()
        global db_obj, current_user
        self.db_obj = db_obj
        self.current_user = current_user
        
        if self.current_user.access_level != 4:
            QMessageBox.critical(self, "Access Denied", "You do not have permission to access the admin dashboard.")
            self.setDisabled(True)
            return
        
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        self.admin_menu= AdminMenu()
        self.admin_menu.add_user.clicked.connect(self.add_user)
        self.admin_menu.delete_user.clicked.connect(self.delete_user)
        layout.addWidget(self.admin_menu)
        # Search section
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by ID, email, or username")
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_user)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        
        # Table
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(6)
        self.user_table.setHorizontalHeaderLabels(["ID", "Username", "Email", "Access Level", "Password", "Rating"])
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


        # Final layout
        layout.addWidget(self.admin_menu)
        layout.addLayout(search_layout)
        layout.addWidget(self.user_table)
        
        self.setLayout(layout)

    def search_user(self):
        search_text = self.search_input.text().strip()
        if not search_text:
            QMessageBox.warning(self, "Input Error", "Please enter an ID, email, or username to search.")
            return
        
        users = self.db_obj.search_user(search_text)
        self.populate_table(users)

    def populate_table(self, users):
        self.user_table.setRowCount(0)
        for user in users:
            row_position = self.user_table.rowCount()
            self.user_table.insertRow(row_position)
            for col, item in enumerate(user):
                self.user_table.setItem(row_position, col, QTableWidgetItem(str(item)))

    def add_user(self):
        dialog = UserFormDialog()
        if dialog.exec_() == QDialog.Accepted:
            dialog.save_user()
    
    def delete_user(self):
        delete_dialog = DeleteUserDialog()
        delete_dialog.exec_()


class MainWind(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        admin = AdminDashboard()
        self.setCentralWidget(admin)
        
if __name__ == "__main__":
    #current_user = db_obj.get_user('hamdanyoumna@gmail.com')
    current_user = db_obj.get_user('test')
    app = QApplication(sys.argv)
    window = MainWind()
    window.setWindowTitle("Smart Design Verification")
    window.setStyleSheet(f'background-color: {body_bg}; font-family: {font_family}; font-size: 16px;')
    window.showMaximized()
    sys.exit(app.exec_())