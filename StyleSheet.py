border_radius = 6
font_family = "Ubuntu"
body_bg = 'white' #"#F5F9FF"
font_size = '16px'
main_blue = '#007BFF'
color = "#565656"

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
                border-color: #0078D7;
            }
            QPushButton {
                background-color: #4169E1;
                color: white;
                font-size: 18px;
                border-radius: 5px;
                padding: 10px;
                height: 40px;
            }
            QPushButton:hover {
                background-color: #0056A3;
            }
        """
        
# Message box style
msg_box_style = """
            QPushButton {
                background-color: #4169E1;
                color: white;
                font-size: 18px;
                border-radius: 5px;
                padding: 10px;
                height: 20px;
                width: 30px;
                border: none;
            }
            """

# Menu styles
menu_bg_color = '#E6F0FF'#'#2C3440'
menu_btn_hover = '#cfe2ff'
menu_btn_click = '#c2d9fc'
menu_border = f'border : 1px solid #d4e4fc;'
menu_btn_style = f"""
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
        """

# Upper menus
upper_menus_style = f"""
            QPushButton {{
                border: none;
                color: black;
                font-size: 18px;
                padding: 5px;
                background-color: {'white'}; 
                font-family:{font_family};
                
            }}
            QPushButton:hover {{
                color: green;
            }}
        """
# Home styles
card_bg = '#E6F7F9'


# Grid styles
panel_bg_color = '#F9F9F9'#'#F4F4F4'
panel_border = 'border : 1px solid #E4E5E8;'

bar_bg = '#4169E1'
bar_bg_empty = '#FAFAFA'
bar_border = f'border : 1px solid #4169E1;'
bar_style_before = f"""
            QProgressBar {{
                border-radius: 6px;
                background-color: {bar_bg_empty};
                height: 16px;
                color: #222222;
                text-align: center;
                {bar_border}
            }}

            QProgressBar::chunk {{
                background-color: {bar_bg};
                border-radius: 5px;
            }}
        """
bar_style_after = f"""
            QProgressBar {{
                border-radius: 6px;
                background-color: {bar_bg_empty};
                height: 16px;
                color: white;
                text-align: center;
                {bar_border}
            }}

            QProgressBar::chunk {{
                background-color: {bar_bg};
                border-radius: 5px;
            }}
        """
status_style = "color: black; padding-right: 10px;"

button_bg = '#6A89A7'
btn_font_color = '#003366'
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
                background-color: {menu_btn_hover};
            }}
            QPushButton:pressed {{
                background-color: {menu_btn_click};
            }}
        """
input_style = f"""
            QLineEdit{{
                font-family: 'Ubuntu';
                font-size: 16px;
                padding: 6px;
                {panel_border}
                border-radius: 4px;
                background-color: white;
                height : 30px;
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
spinbox_style = """
    QSpinBox {
        font-family: 'Ubuntu';
        font-size: 16px;
        padding: 6px;
        border: 1px solid #00786F;
        border-radius: 4px;
        background-color: white;
        height: 30px;
    }    
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
        """
code_editor_bg = '#e4ebf0'
code_editor_border = 'border: 1px solid #D2D3DB;'
code_editor_font_color = 'black'
code_editor_style = f"""
            QPlainTextEdit {{
                background-color: {code_editor_bg};
                font-family: 'Fira Code', 'Courier New', monospace;
                font-size: 20px;
                {code_editor_border}
                color: {code_editor_font_color};
                padding: 12px;
            }}
        """










