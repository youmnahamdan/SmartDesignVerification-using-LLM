border_radius = 6
font_family = "Ubuntu"
body_bg = 'white' #"#F5F9FF"
font_size = '16px'
main_blue = '#006D5B'


# Green button theme
green        = '#2f8a5e'   # main
green_hover  = '#3fae76'   # brighter on hover
green_click  = '#25694a'   # darker on click

# Red button theme
red          = '#992222'   # main
red_hover    = '#b33434'   # brighter on hover
red_click    = '#731818'   # darker on click

# Login styles
login_style_sheet = """
            QWidget {
                background-color: #ffffff;
            }
            QLabel {
                font-size: 18px;
                color: #333;
            }
            QLineEdit {
                height: 44px;
                font-size: 16px;
                padding: 5px;
                border: 2px solid #ccc;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border-color: #006D5B;
            }
            QPushButton {
                background-color: #006D5B;
                color: white;
                font-size: 18px;
                border-radius: 5px;
                padding: 10px;
                height: 40px;
            }
            QPushButton:hover {
                background-color: #046152;
            }
        """
        
# Message box style
msg_box_style = f"""
            QPushButton {{
                background-color: {main_blue};
                color: white;
                font-size: 18px;
                border-radius: 5px;
                padding: 10px;
                height: 20px;
                width: 30px;
                border: none;
            }}
            """

# Menu styles
menu_bg_color = '#FAFAFA'#'#e9edef'#'#E6F0FF'#'#2C3440'
menu_btn_hover = '#b8e3db'
menu_btn_click = '#a6d7ce'
menu_border = f'border : 1px solid #c3c7ca;'
menu_btn_style = f"""
            QPushButton {{
                background-color: transparent;
                color: #4c535e;
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
            QToolTip {{
                background-color: #ffffff;
                color: #333333;
                border: 1px solid #cccccc;
                padding: 6px;
                border-radius: 4px;
                font-family: 'Ubuntu';
                font-size: 16px;
            }}
        """



grid_btn_style = f"""
            QPushButton {{
            color: black;
            font-size: {font_size};
            padding: 10px;
            border-radius: {border_radius};
            }}
            QPushButton:hover {{
            background-color: #F8F8F8;
            }}
            
"""
# Home styles
load_project_style = f"""
QDialog {{
                background-color: #f0f0f0;
                font-family: '{font_family}';
                font-size: 13px;
            }}
            QLabel {{
                font-weight: bold;
                margin-bottom: 4px;
                color: #333;
            }}
            QLineEdit {{
                padding: 6px;
                border: 1px solid #aaa;
                border-radius: 4px;
                font-size: 14px;
            }}
            QPushButton {{
                background-color: #4CAF50;
                color: white;
                padding: 6px 12px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: #45a049;
            }}
"""


# Grid styles
panel_bg_color = '#FAFAFA'#'#F4F4F4'
outer_panel_border = 'border : 1px solid #c3c7ca;'
panel_border = 'border : 1px solid #E4E5E8;'

status_style = "font-family: 'Segoe UI' !important; color: black; padding-right: 10px;font-weight:500;"

button_bg = main_blue #'#003366'
button_hover = '#005245'
button_click = '#003e36'
btn_font_color = '#FFFEF2'
button_style = f"""
            QPushButton {{
                background-color: {button_bg};
                color: {btn_font_color};
                border-radius: 5px;
                padding: 6px 12px;
                font-size: 16px;
                height: 30px;
            }}
            QPushButton:hover {{
                background-color: {button_hover};
            }}
            QPushButton:pressed {{
                background-color: {button_click};
            }}
        """
input_style = f"""
            QLineEdit, QSpinBox{{
                font-family: 'Ubuntu';
                font-size: 16px;
                padding: 6px;
                {panel_border}
                border-radius: 4px;
                background-color: white;
                height : 30px;
            }}
            
            QSpinBox::up-button, QSpinBox::down-button {{
                width: 25px;
                height: 20px;
                padding: 0px;
            }}

            QSpinBox::up-arrow, QSpinBox::down-arrow {{
                width: 8px;
                height: 8px;
            }}
        """
combobox_style = f"""
            QComboBox {{
                font-family: 'Ubuntu';
                font-size: 16px;
                padding: 6px;
                {panel_border}
                border-radius: 4px;
                background-color: white;
                height : 30px;
            }}
            
            /* Style dropdown items */
            QComboBox QAbstractItemView {{
                font-size: 16px;  /* Increased font size for dropdown */
                background-color: white;
                /*selection-background-color: lightgray;*/
                border: 1px solid gray;
                border-radius: 6px;
                padding: 7px; /* Add padding inside dropdown */
            }}

            /* Optional: Space between items in dropdown */
            QComboBox QAbstractItemView::item {{
                padding: 10px;
                font-size: 16px;
                margin: 2px;
            }}
"""
label_style = f"""
            QLabel {{
                font-size: 16px; 
                color: #333; 
                border: none;
            }}
        """
spec_input_style = f"""
            QLineEdit, QTextEdit{{
                font-family: 'Ubuntu';
                font-size: 16px;
                padding: 6px;
                {panel_border}
                border-radius: 4px;
                background-color: white;
                height : 30px;
            }}
            QScrollBar:vertical, QScrollBar:horizontal {{
        background: transparent;
        border: none;
        width: 8px;
        height: 8px;
    }}

    QScrollBar::handle:vertical, QScrollBar::handle:horizontal {{
        background: #cccccc;
        border-radius: 4px;
        min-height: 20px;
        min-width: 20px;
    }}

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        height: 0;
        width: 0;
    }}

    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical,
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
        background: none;
    }}
        """
code_editor_bg = '#fcfdff'
code_editor_border = 'border: 1px solid #D2D3DB;'
code_editor_font_color = 'black'
'''code_editor_style = f"""
            QPlainTextEdit {{
                background-color: {code_editor_bg};
                font-family: 'Fira Code', 'Courier New', monospace;
                font-size: 20px;
                {code_editor_border}
                color: {code_editor_font_color};
                padding: 12px;
            }}
        """'''
        
code_editor_style = f"""
QPlainTextEdit {{
    background-color: #2a2d2e;  /* Lighter than #1e1e1e */
    color: #dcdcdc;
    font-family: Consolas, Courier New, monospace;
    border: 1px solid #cccccc33;  /* subtle light gray border */
    border-radius: 8px;
    padding: 6px;
}}
QScrollBar:vertical, QScrollBar:horizontal {{
    background: transparent;
    border: none;
    width: 8px;
    height: 8px;
}}

QScrollBar::handle:vertical, QScrollBar::handle:horizontal {{
    background: #cccccc;
    border-radius: 4px;
    min-height: 20px;
    min-width: 20px;
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    height: 0;
    width: 0;
}}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical,
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
    background: none;
}}
"""














# Upper menus
upper_menus_style = f"""
            QPushButton {{
                border: none;
                color: black;
                font-size: 16px;
                padding: 5px;
                background-color: {'white'}; 
                font-family:{font_family};
                
            }}
            QPushButton:hover {{
                color: #003366;
            }}
        """

prompt_menu_bg = "#F6F6F6"
home_menu_bg = "#F8F8F8"
button_hover = "#0c4a87"
home_menu_style = f"""
            QPushButton {{
                border: none;
                color: black;
                font-size: 16px;
                padding: 5px;
                font-family:{font_family};
                
            }}
            QPushButton:hover {{
                color: {button_hover};
            }}
        """

admin_menu_style = f"""
            QPushButton {{
                border: none;
                color: black;
                font-size: 16px;
                padding: 5px;
                font-family:{font_family};
                
            }}
            QPushButton:hover {{
                color: #003366;
            }}
        """



# Admin styles
search_button_style = f"""
            QPushButton {{
                background-color: {panel_bg_color};
                color: {main_blue};
                font-size: 16px;
                border-radius: {border_radius}px;
                {panel_border}
                padding: 6px 12px;
                height: 30px;
            }}
            QPushButton:hover {{
                background-color: {panel_bg_color};
            }}
"""

search_input_style = f"""
            QLineEdit {{
                font-size: 16px;
                padding: 6px 12px;
                height: 30px;
            }}
"""


user_dialog_style  =f"""
    QWidget {{
        font-family: 'Ubuntu';
        font-size: 15px;
    }}

    {input_style}

    {label_style}

    QDialog {{
        background-color: #ffffff;
    }}

    QTableWidget {{
        border: 1px solid #ccc;
        gridline-color: #eee;
        selection-background-color: #87cefa;
        selection-color: #000;
    }}

    QHeaderView::section {{
        background-color: #f0f0f0;
        padding: 6px;
        border: 1px solid #ccc;
        font-weight: bold;
    }}
"""

delete_dialog_style = f"""
    QWidget {{
        background-color: #ffffff;
        font-family: 'Ubuntu';
        font-size: {font_size};
    }}

    {label_style}

    {input_style}

    QPushButton {{
        background-color: {red};
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 6px;
        height: 20px;
    }}

    QPushButton:hover {{
        background-color: {red_hover};
    }}

    QPushButton:pressed {{
        background-color: {red_click};
    }}
"""


table_border = '#ededed'
table_bg = '#fbfbfb'
table_font_family = 'Segoe UI'  # Or 'Segoe UI', 'Roboto'


home_table_style = """
QTableWidget {
    background-color: #fbfbfb;  /* Full table background */
    border: 1px solid #e6e8ea;
    border-radius: 12px;
    font-family: 'Segoe UI', 'Inter', sans-serif;
    font-size: 15px;
    color: #333;
    gridline-color: #f0f1f2;
}

QTableWidget::viewport {
    background-color: #fbfbfb;
    border-radius: 12px;
}

QHeaderView::section {
    background-color: #fbfbfb;
    color: #555;
    padding: 8px;
    font-weight: 600;
    font-size: 15px;
    border: none;
    border-bottom: 1px solid #e6e8ea;
    font-family: 'Segoe UI', 'Inter', sans-serif;
}

QTableWidget::item {
    padding: 8px;
    border: none;
    font-size: 20px;
    font-family: 'Segoe UI', 'Inter', sans-serif;
    background-color: transparent;
    color: #333;
}

QTableView::item {
    font-size: 20px;
    font-family: 'Segoe UI', 'Inter', sans-serif;
    color: #333;
}

QTableWidget::item:selected {
    background-color: #a6d7ce; 
    color: #1a1a1a;
    border-radius: 8px;
}

QTableWidget::item:hover {
    background-color: #f6f6f6;
}

QScrollBar:vertical, QScrollBar:horizontal {
    background: transparent;
    border: none;
    width: 6px;
    height: 6px;
}

QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
    background: #d0d2d3;
    border-radius: 3px;
    min-height: 20px;
    min-width: 20px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    height: 0;
    width: 0;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical,
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
}
"""



project_dia_style= dialog_style = """
QDialog {
    background-color: #f9f9f9;
    border: 1px solid #dcdcdc;
    border-radius: 10px;
    padding: 10px;
}

QLabel {
    font-size: 13px;
    color: #333;
    padding: 2px;
}

QLineEdit {
    background-color: #ffffff;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 5px;
    font-size: 13px;
}

QLineEdit:focus {
    border: 1px solid #5cabff;
}

QComboBox {
    background-color: #ffffff;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 5px;
    font-size: 13px;
}

QComboBox:focus {
    border: 1px solid #5cabff;
}

QPushButton {
    background-color: #5cabff;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 6px 12px;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #4791db;
}

QPushButton:pressed {
    background-color: #3b7ec6;
}

QSpinBox {
    background-color: #ffffff;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 5px;
    font-size: 13px;
}

QSpinBox:focus {
    border: 1px solid #5cabff;
}
"""



save_button_style  = f"""
            QPushButton {{
                background-color: {main_blue};
                color: {btn_font_color};
                border-radius: 5px;
                padding: 6px 12px;
                font-size: 16px;
                height: 30px;
            }}
            QPushButton:hover {{
                background-color: {green_hover};
            }}
            QPushButton:pressed {{
                background-color: {green_click};
            }}
        """
cancel_button_style = f"""
    QPushButton {{
        background-color: {red};
        color: {btn_font_color};
        border-radius: 5px;
        padding: 6px 12px;
        font-size: 16px;
        height: 30px;
    }}
    QPushButton:hover {{
        background-color: {red_hover};
    }}
    QPushButton:pressed {{
        background-color: {red_click};
    }}
"""
restore_button_style = f"""
            QPushButton {{
                background-color: {red};
                color: {btn_font_color};
                border-radius: 5px;
                padding: 6px 12px;
                font-size: 16px;
                height: 30px;
            }}
            QPushButton:hover {{
                background-color: {red_hover};
            }}
            QPushButton:pressed {{
                background-color: {red_click};
            }}
        """




  
  



user_table_style = """
    QTableWidget {
        font-family: 'Ubuntu';
        background-color: #ffffff;
        gridline-color: #dddddd;
        font-size: 14px;
        border: 1px solid #cccccc;
    }

    QHeaderView::section {
        background-color: #fafafa;
        color: #333333;
        font-weight: 400;
        padding: 6px;
        border: 1px solid #dddddd;
    }

    QTableWidget::item {
        padding: 6px;
        border: none;
    }

    QTableWidget::item:selected {
        background-color: #a6d7ce;
        color: #000;
    }

    QTableCornerButton::section {
        background-color: #f0f0f0;
        border: 1px solid #dddddd;
    }
"""





log_output_style = """
QTextEdit {
    background-color: #1e1e1e;
    color: #dcdcdc;
    border: 1px solid #555;
    padding: 6px;
    font-family: Consolas, monospace;
    font-size: 14px;      
    line-height: 1.6em;         
}
QScrollBar:vertical, QScrollBar:horizontal {{
    background: transparent;
    border: none;
    width: 8px;
    height: 8px;
}}

QScrollBar::handle:vertical, QScrollBar::handle:horizontal {{
    background: #cccccc;
    border-radius: 4px;
    min-height: 20px;
    min-width: 20px;
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    height: 0;
    width: 0;
}}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical,
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
    background: none;
}}
"""

code_editor_btn = """
QPushButton {
            background-color: #2d2d30;
            color: white;
            border: 1px solid #3e3e42;
            border-radius: 5px;
            padding: 5px 10px;
        }
        QPushButton:hover {
            background-color: #3e3e42;
        }
        QPushButton:pressed {
            background-color: #505053;
        }
"""