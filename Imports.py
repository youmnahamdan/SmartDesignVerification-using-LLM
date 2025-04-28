# Built-in imports
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys


# Project imports
from SVAISystem import * 
from config import eda_output_data_formats, proj_config, fpga_boards, simulation_tools  
from scripting import *
from db_access import db_access
from StyleSheet import *
from WorkerThread import *

# Qt imports
from PyQt5.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal, pyqtSlot

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QTextEdit, 
    QPushButton, QVBoxLayout, QFormLayout, QHBoxLayout, QProgressBar, 
    QComboBox, QGridLayout, QMessageBox, QFrame, QCheckBox, QAction,
    QDoubleSpinBox, QTableWidgetItem, QTableWidget,  QSpinBox, QHeaderView,
    QSizePolicy, QPlainTextEdit, QFileDialog
)
from PyQt5.QtGui import QFont, QIcon, QColor, QSyntaxHighlighter, QTextCharFormat, QPainter, QLinearGradient, QBrush, QPainterPath
from PyQt5.QtCore import Qt, QSize, QRegularExpression, QRectF, QTimer
from concurrent.futures import ThreadPoolExecutor


# Global 

db_obj = db_access()
current_user = None
executor = ThreadPoolExecutor(max_workers=6)  # Keep this global or in the class
feedback_cycles = 3

status_label = None
progress_bar = None
def register_ui(status, progress):
    global status_label, progress_bar
    status_label = status
    progress_bar = progress

def update_status_and_progress(text=None, value=None):
    if status_label is not None and text is not None:
        status_label.setText(f"Status: {text}")
    if progress_bar is not None:
        if value is not None:
            progress_bar.setValue(value)
        
def setWidgetBG(layout, bg_color, left_m = 0, top_m = 0, right_m = 0, bottom_m = 0, border = "", border_radius = border_radius):
    
    layout_widget = QWidget()
    layout_widget.setLayout(layout)
    layout_widget.setContentsMargins(left_m + 30, top_m, right_m + 30 , bottom_m)
    layout_widget.setStyleSheet(f"background-color: {bg_color}; padding: 0px;  border-radius : {border_radius}px; {border};")


    main_layout = QVBoxLayout()
    main_layout.addWidget(layout_widget)
    main_layout.setContentsMargins(0, 0, 0, 0)  # Remove extra margins
    main_layout.setSpacing(0)  # Ensure no extra space between widgets
    return main_layout
    



def create_msg_box(parent, icon, title, text):
    msg_box = QMessageBox(parent)
    msg_box.setIcon(icon)
    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.setStyleSheet(msg_box_style)
    msg_box.exec_()
    return