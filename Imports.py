# Built-in imports
#from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.figure import Figure
import sys
    

# Project imports
import config 
from scripting import *
from StyleSheet import *
from WorkerThread import *
import session 

# Qt imports
from PyQt5.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal, pyqtSlot, QEvent

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QTextEdit, 
    QPushButton, QVBoxLayout, QFormLayout, QHBoxLayout, QProgressBar, 
    QComboBox, QGridLayout, QMessageBox, QFrame, QCheckBox, QAction,
    QDoubleSpinBox, QTableWidgetItem, QTableWidget,  QSpinBox, QHeaderView,
    QSizePolicy, QPlainTextEdit, QFileDialog , QDialog, QSpacerItem, QStackedLayout,
    QShortcut, QToolTip
    
)
from PyQt5.QtGui import QFont, QIcon, QColor, QSyntaxHighlighter, QTextCharFormat, QPainter, QLinearGradient, QBrush, QPainterPath, QTextCursor, QKeySequence, QPixmap, QTextFormat
from PyQt5.QtCore import Qt, QRectF, QTimer, QRect, QSize, QRegularExpression


status_label = None
def register_ui(status):
    global status_label
    status_label = status
            
def update_status_and_progress(text=None, color='black'):
    if status_label is not None and text is not None:
        status_label.setText(f"Status: {text}")
        status_label.setStyleSheet(f"font-family: 'Segoe UI' !important; color: {color}; padding-right: 10px;font-weight:500;")
    
        
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


def display_output(title, message):
    """Show a PyQt5 message box from non-GUI classes."""
    app = QApplication.instance()
    owns_app = False

    if app is None:
        # Create a new QApplication if none exists
        app = QApplication(sys.argv)
        owns_app = True

    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setIcon(QMessageBox.Information)
    msg_box.exec_()

    if owns_app:
        app.quit()