from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QApplication
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys

class ProjectWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(self.widget_style())
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Table
        self.table = QTableWidget(5, 2)
        self.table.setHorizontalHeaderLabels(["Project Name", "Last Modified"])
        self.table.setStyleSheet(self.table_style())
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setFont(QFont("Segoe UI", 10))

        for i in range(5):
            self.table.setItem(i, 0, QTableWidgetItem(f"Project {i+1}"))
            self.table.setItem(i, 1, QTableWidgetItem("2025-06-02"))

        # Buttons
        button_layout = QHBoxLayout()
        buttons = ["Open", "New", "Delete Project"]
        for label in buttons:
            btn = QPushButton(label)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(self.button_style())
            button_layout.addWidget(btn)

        layout.addWidget(self.table)
        layout.addLayout(button_layout)

    def widget_style(self):
        return """
        QWidget {
            background-color: #e9edef;
            border: 1px solid #c3c7ca;
            border-radius: 8px;
        }
        """

    def table_style(self):
        return """
        QTableWidget {
            background-color: #f7f9fa;
            border: 1px solid #c3c7ca;
            border-radius: 6px;
            gridline-color: #d0d4d7;
        }
        QHeaderView::section {
            background-color: #dde1e4;
            padding: 4px;
            font-weight: bold;
            border: 1px solid #c3c7ca;
        }
        QTableWidget::item:selected {
            background-color: #cfd3d6;
        }
        """

    def button_style(self):
        return """
        QPushButton {
            background-color: #cfd3d6;
            color: #2e3a40;
            border: 1px solid #c3c7ca;
            border-radius: 5px;
            padding: 6px 12px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #dbe0e3;
        }
        QPushButton:pressed {
            background-color: #bcc2c5;
        }
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProjectWidget()
    window.resize(600, 400)
    window.setWindowTitle("Project Manager")
    window.show()
    sys.exit(app.exec_())
