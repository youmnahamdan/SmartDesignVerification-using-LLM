from Imports import  *
from ProjectFlowUI import *

class SystemVerilogHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#653577"))
        keyword_format.setFontWeight(QFont.Bold)

        keyword_patterns = [
            r"\bmodule\b", r"\bendmodule\b", r"\binput\b", r"\boutput\b", r"\binout\b", r"\bwire\b", r"\breg\b",
            r"\blogic\b", r"\balways\b", r"\balways_ff\b", r"\balways_comb\b", r"\balways_latch\b", r"\bassign\b",
            r"\bbegin\b", r"\bend\b", r"\bif\b", r"\belse\b", r"\bcase\b", r"\bendcase\b", r"\bdefault\b",
            r"\bfor\b", r"\bwhile\b", r"\brepeat\b", r"\bforever\b", r"\bgenerate\b", r"\bendgenerate\b",
            r"\bgenvar\b", r"\bparameter\b", r"\blocalparam\b", r"\bfunction\b", r"\bendfunction\b",
            r"\btask\b", r"\bendtask\b", r"\breturn\b", r"\bposedge\b", r"\bnegedge\b", r"\btypedef\b",
            r"\bstruct\b", r"\bendstruct\b", r"\benum\b", r"\bendinterface\b", r"\binterface\b", r"\bpackage\b",
            r"\bendpackage\b", r"\bimport\b", r"\bexport\b", r"\bconst\b", r"\bstatic\b"
        ]


        self.highlighting_rules = [(QRegularExpression(pat), keyword_format) for pat in keyword_patterns]

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#FE099D"))
        self.highlighting_rules.append((QRegularExpression(r'"[^"]*"'), string_format))

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#1B3644"))
        self.highlighting_rules.append((QRegularExpression(r"//.*"), comment_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                match = it.next()
                start, length = match.capturedStart(), match.capturedLength()
                self.setFormat(start, length, fmt)

class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(code_editor_style)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        font = QFont("Fira Code", 16)
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)

        # Enable syntax highlighting
        self.highlighter = SystemVerilogHighlighter(self.document())

class CodeEditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.editor = CodeEditor()

        # Buttons
        self.open_button = QPushButton("Open File")
        self.save_button = QPushButton("Save File")
        
        self.open_button.setStyleSheet(button_style)
        self.save_button.setStyleSheet(button_style)

        self.open_button.clicked.connect(self.open_file)
        self.save_button.clicked.connect(self.save_file)

        # Layouts
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.open_button)
        button_layout.addWidget(self.save_button)
        
        layout = QVBoxLayout()
        layout.addWidget(self.editor)
        layout.addLayout(button_layout)
        

        self.setLayout(layout)
        self.setStyleSheet(f"background-color: {code_editor_bg};")

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "SystemVerilog Files (*.sv *.v);;All Files (*)")
        if path:
            try:
                with open(path, 'r') as f:
                    self.editor.setPlainText(f.read())
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to open file:\n{str(e)}")

    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "SystemVerilog Files (*.sv *.v);;All Files (*)")
        if path:
            try:
                with open(path, 'w') as f:
                    f.write(self.editor.toPlainText())
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to save file:\n{str(e)}")



class GradientCard(QFrame):
    def __init__(self, title, number, change, icon=None, gradient_colors=None):
        super().__init__()
        self.setFixedSize(150, 150)
        self.title = title
        self.number = number
        self.change = change
        self.gradient_colors = gradient_colors or [(255, 200, 255), (200, 220, 255)]
        self.setContentsMargins(10, 10, 10, 10)
        self.setFixedSize(175, 175)       # min square
        
        layout = QVBoxLayout()
        layout.setSpacing(0)

        title_label = QLabel(title)
        title_label.setFont(QFont("Ubuntu", 10))
        title_label.setStyleSheet("color: #444; background: none;")
        layout.addWidget(title_label)

        number_label = QLabel(str(number))
        number_label.setFont(QFont("Ubuntu", 30, QFont.Weight.Bold))
        number_label.setStyleSheet("background: none;")

        layout.addWidget(number_label)

        change_label = QLabel(f"+{change} last day")
        change_label.setFont(QFont("Ubuntu", 9))
        change_label.setStyleSheet("color: gray; background: none;")
        layout.addWidget(change_label)

        layout.addStretch()
        self.setLayout(layout)

    def paintEvent(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRectF(self.rect())
        path = QPainterPath()
        path.addRoundedRect(rect, border_radius, border_radius)

        painter.setClipPath(path)
        gradient = QLinearGradient(rect.topLeft(), rect.bottomRight())
        for i, color_hex in enumerate(self.gradient_colors):
            gradient.setColorAt(i / (len(self.gradient_colors) - 1), QColor(color_hex))
        painter.fillRect(rect, QBrush(gradient))
        
        painter.end()

class HomeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background-color: {body_bg};")

        # Main layout (vertical, top for user card & plot, bottom for buttons & info)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # Both buttons will redirect to project setup
        self.create_project_btn = QPushButton("Create New Project")
        #create_project_btn.clicked.connect(self.create_project) 
        
        self.open_project_btn = QPushButton("Open Project")
        #open_project_btn.clicked.connect(self.open_project)
        
        main_layout.addWidget(self.create_project_btn, 1)
        main_layout.addWidget(self.open_project_btn, 1)

        '''# Upper section: user info card and bar chart
        left_layout = QVBoxLayout()
        user_card = self.create_user_card(name="John Doe", user_id="12345", email="john.doe@example.com", access_level="4")
        left_layout.addLayout(user_card)
        left_layout.setSpacing(10)
        left_layout.setContentsMargins(0, 0, 0, 0)
        chart = self.create_bar_chart()
        left_layout.addWidget(chart, 3)

        # Add upper section to the main layout
        main_layout.addLayout(left_layout, 5)

        # Bottom section: project details and buttons
        right_layout = QVBoxLayout()
        right_layout.setSpacing(15)

        # Project info section
        project_info = QLabel("HI")
        right_layout.addWidget(project_info)


        # Add bottom section to main layout
        main_layout.addLayout(right_layout, 3)'''

        self.setLayout(main_layout)

    def create_user_card(self, name, user_id, email, access_level):
        Hello_label = QLabel(f"Hello,")
        Hello_label.setStyleSheet(f"font-size: 40px; padding: 0px 20px; color: gray;")
        name_label = QLabel(f"{name}.")
        name_label.setStyleSheet(f"font-size: 40px; padding: 0px 20px; color: {main_blue};")
        
        card_layout = QVBoxLayout()
        card_layout.addWidget(Hello_label)
        card_layout.addWidget(name_label)
        card_layout.addSpacing(20)

        layout = QHBoxLayout()

        views_card = GradientCard("No. Projects", 31, 3, gradient_colors=["#CBA4FF", "#DCF7FF"])
        clients_card = GradientCard("Acess Level", 4, 1, gradient_colors=["#A4E6FF", "#E0F8FF"])
        purchases_card = GradientCard("Rating", 4.3, 1, gradient_colors=["#FFFFFF", "#F0F0F0"])

        layout.addWidget(views_card)
        layout.addWidget(clients_card)
        layout.addWidget(purchases_card)
        
        card_layout.addLayout(layout)

        return card_layout

    def create_bar_chart(self):
        # Sample data for daily API calls
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        calls = [120, 98, 110, 130, 115, 80, 60]

        fig = Figure(figsize=(5, 4))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)

        ax.bar(days, calls, color='#0ABAC6')
        ax.set_title("Daily API Calls")
        ax.set_ylabel("Number of Calls")
        ax.set_xlabel("Day of the Week")
        ax.grid(True, linestyle='--', alpha=0.3)

        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return canvas

    def create_project_info(self):
        # Sample project information
        projects_count = 5

        project_info_frame = QFrame()
        project_info_frame.setStyleSheet("""
            QFrame {
                background-color: #CCE5FF;
                border-radius: 12px;
                padding: 15px;
            }
        """)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Projects: {projects_count}"))
        layout.addWidget(QLabel("Create a new project, or open an existing one."))

        project_info_frame.setLayout(layout)
        return project_info_frame

    def create_action_buttons(self):
        button_layout = QGridLayout()

        # Create Buttons
        new_project_button = QPushButton("Create New Project")
        open_project_button = QPushButton("Open Project")
        change_password_button = QPushButton("Change Password")

        # Button Styling
        for button in [new_project_button, open_project_button, change_password_button]:
            button.setStyleSheet("""
                QPushButton {
                    background-color: #0ABAC6;
                    color: white;
                    border-radius: 8px;
                    padding: 10px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #007BFF;
                }
            """)

        # Adding Buttons to Grid Layout
        button_layout.addWidget(new_project_button, 0, 0)
        button_layout.addWidget(open_project_button, 0, 1)
        button_layout.addWidget(change_password_button, 1, 0, 1, 2)

        return button_layout
    
class SideMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(100)
        self.setStyleSheet("""
            color: white;  /* White text */
        """)

        # Create a vertical layout
        layout = QVBoxLayout()
        layout.setSpacing(20)  # Space out the buttons equally

        # Add buttons
        self.add_menu_button(layout, "", parent.show_home_widget, "icons/icons8-home-32.png")
        self.add_menu_button(layout, "", parent.show_project_setup, "icons/icons8-setup-32.png")
        self.add_menu_button(layout, "", parent.show_code_editor, "icons/icons8-code-windows-metro-70.png")
        self.add_menu_button(layout, "", parent.show_analysis, "icons/icons8-analysis-32.png")

        layout.addStretch()  # Push buttons upwards
        self.add_menu_button(layout, "", parent.show_dashboard_ui, "icons/icons8-dashboard-32.png")
        self.add_menu_button(layout, "", parent.show_profile_ui, "icons/icons8-male-user-32.png")
        
        
        self.setLayout(setWidgetBG(layout, menu_bg_color,  -30, 15, -30, 15, border=menu_border))
        
        
    def add_menu_button(self, layout, text, function, icon_dir):
        """Helper function to add a menu button"""
        button = QPushButton(text)
        button.setIcon(QIcon(icon_dir))  # Replace with your icon path
        button.setIconSize(QSize(24, 24)) 
        
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: white;
                font-size: 16px;
                padding: 10px;
                border: none;
                text-align: left;
            }}                
            QPushButton:hover {{
                background-color: {menu_btn_hover};  /* Lighter blue on hover */ 
            }}
            QPushButton:pressed {{ 
                background-color: {menu_btn_click};  /* Even darker blue when pressed */
            }}
        """)
        button.clicked.connect(function)
        layout.addWidget(button, alignment=Qt.AlignHCenter)

"""class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Design Verification using LLM")
        self.setStyleSheet(f'background-color: {body_bg}; font-family: {font_family}; font-size: 16px;')

        login_wid = LoginWidget()
        main_lay = QHBoxLayout()
        main_lay.addWidget(login_wid)
        self.setLayout(main_lay)

        '''# Central container widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout inside central widget
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Side menu
        self.side_menu = SideMenu(self)
        main_layout.addWidget(self.side_menu)

        # Main content area
        self.content_area = QWidget()
        self.content_area.setStyleSheet("background-color: white;")
        self.content_area_layout = QVBoxLayout()
        self.content_area_layout.setContentsMargins(0, 0, 0, 0)
        self.content_area.setLayout(self.content_area_layout)
        main_layout.addWidget(self.content_area)

        # Widgets to switch between
        self.grid_widget = GridWidget(parent=self )
        self.code_widget = CodeEditorWidget(parent=self)'''

    def show_home_widget(self):
        self.set_new_widget(HomeWidget())

    def show_profile_ui(self):
        print("Generate UI clicked")

    def show_dashboard_ui(self):
        print("Dashboard clicked")

    def show_code_editor(self):
        self.set_new_widget(self.code_widget)

    def show_analysis(self):
        print("Profile clicked")

    def show_project_setup(self):
        self.set_new_widget(self.grid_widget)

    def set_new_widget(self, new_widget):
        '''Replace the central widget with a new one.'''
        # Clear existing widgets from `content_area_layout`
        for i in reversed(range(self.content_area_layout.count())):
            widget_to_remove = self.content_area_layout.itemAt(i).widget()
            if widget_to_remove:
                widget_to_remove.setParent(None)

        # Add the new widget
        new_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.content_area_layout.addWidget(new_widget)
        self.content_area.update()"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Design Verification using LLM")
        self.setStyleSheet(f'background-color: {body_bg}; font-family: {font_family}; font-size: 16px;')

        # Start with login widget
        self.login_widget = LoginWidget()
        self.setCentralWidget(self.login_widget)

        # Prepare the "post-login" widgets, but don't add them yet
        self.init_main_ui()

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
        self.content_area.setStyleSheet("background-color: white;")
        self.content_area_layout = QVBoxLayout()
        self.content_area_layout.setContentsMargins(0, 0, 0, 0)
        self.content_area.setLayout(self.content_area_layout)
        main_layout.addWidget(self.content_area)

        # Widgets to switch between
        self.grid_widget = GridWidget(parent=self)
        self.code_widget = CodeEditorWidget(parent=self)

    def on_login_success(self):
        """Called when login is successful."""
        self.setCentralWidget(self.main_container)
        self.show_home_widget()

    def show_home_widget(self):
        self.set_new_widget(HomeWidget())

    def show_profile_ui(self):
        print("Generate UI clicked")

    def show_dashboard_ui(self):
        print("Dashboard clicked")

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

        new_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.content_area_layout.addWidget(new_widget)
        self.content_area.update()

# --- Main execution ---
if __name__ == "__main__":
    settings = {
        "PROJECT_DIRECTORY": 'C:/Users/hp/OneDrive/Desktop/SDV/projects/self_testing_and',
        "PROJECT_NAME": 'self_testing_and',
        "TOP_LEVEL_ENTITY": 'self_testing_and',
        "TEST_BENCH_NAME": 'tb_self_testing_and',
    }

    for key, value in settings.items():
        proj_config.set(key, value)

    app = QApplication([])
    window = MainWindow()
    window.showMaximized()
    app.exec_()

