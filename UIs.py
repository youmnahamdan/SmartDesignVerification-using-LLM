from ctypes import alignment
from Imports import  *
from ProjectFlowUI import *
from UserManagementSystem import *

class SideMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(100)
        self.setStyleSheet("""
            color: white;  /* White text */
        """)

        # Create a vertical layout
        layout = QVBoxLayout()
        layout.setSpacing(30)  # Space out the buttons equally

        # Add buttons
        self.add_menu_button(layout, "", parent.show_home_widget, "icons/icons8-home-60.png")
        self.add_menu_button(layout, "", parent.show_project_setup, "icons/icons8-project-60.png")
        self.add_menu_button(layout, "", parent.show_code_editor, "icons/icons8-code-52.png")
        self.add_menu_button(layout, "", parent.show_analysis, "icons/icons8-analysis-60.png")

        layout.addStretch()  # Push buttons upwards
        self.add_menu_button(layout, "", parent.show_dashboard_ui, "icons/icons8-dashboard-60.png")
        
        
        self.setLayout(setWidgetBG(layout, menu_bg_color,  -30, 15, -30, 15, border=menu_border))
        
        
    def add_menu_button(self, layout, text, function, icon_dir):
        """Helper function to add a menu button"""
        button = QPushButton(text)
        button.setIcon(QIcon(icon_dir))  # Replace with your icon path
        button.setIconSize(QSize(30, 30)) 
        
        button.setStyleSheet(menu_btn_style)
        button.clicked.connect(function)
        layout.addWidget(button, alignment=Qt.AlignHCenter)

class fakemain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {body_bg}; font-family: '{font_family}'; font-size: {font_size}; color: {color};")
        self.main_container = QWidget()
        main_layout = QHBoxLayout(self.main_container)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Side menu
        self.side_menu = SideMenu(self)
        main_layout.addWidget(self.side_menu)

        # Main content area
        self.content_area = QWidget()
        self.content_area_layout = QVBoxLayout()
        self.content_area_layout.setContentsMargins(0, 0, 0, 0)
        self.content_area.setLayout(self.content_area_layout)
        main_layout.addWidget(self.content_area)
        self.setCentralWidget(self.main_container)
        
    def show_home_widget(self):
        print("Generate UI clicked")

    def show_profile_ui(self):
        print("Generate UI clicked")

    def show_dashboard_ui(self):
        print("Generate UI clicked")

    def show_code_editor(self):
        print("Generate UI clicked")

    def show_analysis(self):
        print("Profile clicked")

    def show_project_setup(self):
        print("Generate UI clicked")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Design Verification using LLM")
        self.setStyleSheet(f'background-color: {body_bg}; font-family: {font_family}; font-size: 16px;')

        # Start with login widget
        self.login_widget = LoginWidget()
        self.login_widget.login_successful.connect(self.on_login_success)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addStretch()
        layout.addWidget(self.login_widget, alignment=Qt.AlignCenter)
        layout.addStretch()

        self.setCentralWidget(container)

        # Prepare the "post-login" widgets, but don't add them yet
        self.init_main_ui()
        
        #remove
        self.login_widget.login_successful.emit()  # Simulate a successful login for testing purposes

        


    def init_main_ui(self):
        """Prepare the main UI (menu + content), but don't show it yet."""
        self.main_container = QWidget()
        main_layout = QHBoxLayout(self.main_container)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Side menu
        self.side_menu = SideMenu(self)
        main_layout.addWidget(self.side_menu)

        # Main content area
        self.content_area = QWidget()
        self.content_area_layout = QVBoxLayout()
        self.content_area_layout.setContentsMargins(0, 0, 0, 0)
        self.content_area.setLayout(self.content_area_layout)
        main_layout.addWidget(self.content_area)

        # Widgets to switch between
        self.grid_widget = GridWidget(parent=self)
        self.grid_widget.hide()
        self.code_widget = None#CodeEditorWidget(parent=self)

    def on_login_success(self):
        """Called when login is successful."""
        if getattr(self.login_widget, "login_successful", False):
            print("Login successful:", self.login_widget.login_successful)
        
            # Remove the login widget and show the main app
            self.login_widget.setParent(None)  # Optional: safely remove old widget

            # Set the main UI
            self.setCentralWidget(self.main_container)

            # Show default page after login
            self.show_home_widget()

    def show_home_widget(self):
        label = QLabel("Welcome to Smart Design Verification")
        self.set_new_widget(label)#HomeWidget())

    def show_profile_ui(self):
        print("Generate UI clicked")

    def show_dashboard_ui(self):
        self.set_new_widget(AdminDashboard())

    def show_code_editor(self):
        self.set_new_widget(self.code_widget)

    def show_analysis(self):
        print("Profile clicked")

    def show_project_setup(self):
        self.set_new_widget(self.grid_widget)

    def set_new_widget(self, new_widget):
        """Replace the central widget with a new one."""
        for i in reversed(range(self.content_area_layout.count())):
            widget_to_remove = self.content_area_layout.itemAt(i).widget()
            if widget_to_remove:
                widget_to_remove.setParent(None)

        new_widget.show()
        new_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.content_area_layout.addWidget(new_widget)
        self.content_area.update()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.showMaximized()
    sys.exit(app.exec_())