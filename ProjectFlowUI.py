from Imports import *
from DataClasses import *
import session
import config
from SVAISystem import * 


class EmulationMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QHBoxLayout()
        layout.setSpacing(10)  # Adjust spacing between buttons
        
        # Button Definitions
        self.compile_btn = self.create_button(" Compile", "icons/icons8-triangle-32.png")
        self.waveform_btn = self.create_button(" Display Waveform", "icons/sound-wave.png")
        self.emulate_btn = self.create_button("  Emulate", "icons/cpu.png")
        
        # Add buttons to layout
        layout.addWidget(self.compile_btn)
        layout.addWidget(self.waveform_btn)
        layout.addWidget(self.emulate_btn)
        
        

        # Set layout
        self.setLayout(setWidgetBG(layout, 'white', -30, 0, -30, 0, border_radius = 5))

    def create_button(self, text, icon_path):
        button = QPushButton(text)
        button.setIcon(QIcon(icon_path))
        button.setStyleSheet(upper_menus_style)
        button.setIconSize(QSize(28, 28)) 
        return button
    
            
class TerminalWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Terminal Output Area (Read-Only)
        self.terminal_output = QPlainTextEdit()
        self.terminal_output.setReadOnly(True)
        self.terminal_output.setFont(QFont("Consolas", 10))
        self.terminal_output.setStyleSheet(f"""
            background-color: white;
            color: #333;
            {panel_border}
            padding: 5px;
            border-radius : 5;                                 
        """)
        
        self.layout.addWidget(self.terminal_output)
        self.layout.setContentsMargins(0,0,0,0)
        
        self.setLayout(self.layout)

    def append_text(self, text):
        """Adds new text to the terminal output"""
        self.terminal_output.appendPlainText(text)

class Emulation(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.threadpool = QThreadPool()
        self.current_worker = None
        self.init_ui()

    def init_ui(self):
        # Emulation menu
        self.emu_menu = EmulationMenu()
        self.emu_menu.emulate_btn.clicked.connect(self.emulate)
        self.emu_menu.compile_btn.clicked.connect(self.compile_project)
        self.emu_menu.waveform_btn.clicked.connect(self.display_waveform)
        
        # Grid Layout for Inputs
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        # Directory Selection
        self.file_label = QLabel("Pin Assignment File:")
        self.file_label.setStyleSheet(label_style)
        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("Pin Assignment File Path")
        self.file_input.setStyleSheet(input_style)
        self.choose_button = QPushButton("Choose")
        self.choose_button.setStyleSheet(button_style)
        self.choose_button.clicked.connect(self.choose_file)
        grid_layout.addWidget(self.file_label, 0, 0)
        grid_layout.addWidget(self.file_input, 0, 1)
        grid_layout.addWidget(self.choose_button, 0, 2)
        
        # Cable Index
        cable_label = QLabel("Cable Index:")
        cable_label.setStyleSheet(label_style)
        self.cable_input = QSpinBox()
        self.cable_input.setStyleSheet(input_style)
        self.cable_input.setRange(0, 10)  # Assuming max 10 cables
        
        
        # Programming Mode
        mode_label = QLabel("Programming Mode:")
        mode_label.setStyleSheet(label_style)
        self.mode_input = QLineEdit()
        self.mode_input.setStyleSheet(input_style)
         
        # JTAG Device Index
        device_label = QLabel("JTAG Device Index:")
        device_label.setStyleSheet(label_style)
        self.device_input = QSpinBox()
        self.device_input.setStyleSheet(input_style)
        self.device_input.setRange(0, 10)  # Assuming max 10 devices
        
        settings_layout = QHBoxLayout()
        settings_layout.addWidget(cable_label)
        settings_layout.addWidget(self.cable_input)
        settings_layout.addSpacing(30)
        settings_layout.addWidget(device_label)
        settings_layout.addWidget(self.device_input)
        settings_layout.addSpacing(30)
        settings_layout.addWidget(mode_label)
        settings_layout.addWidget(self.mode_input)

        # SOF check
        sof_layout = QHBoxLayout()
        self.sof_label = QLabel("SOF file directory:")
        self.sof_label.setStyleSheet(label_style)
        self.sof_dir = QLineEdit()
        self.sof_dir.setReadOnly(True)
        self.sof_dir.setStyleSheet(input_style)
        self.sof_status = QLabel("Not Found") 
        self.sof_status.setStyleSheet(label_style)
        self.sof_status.setFont(QFont("Arial", 10, QFont.Bold))
        self.sof_status.setStyleSheet("color: red; border:none;")
        sof_layout.addWidget(self.sof_label)
        sof_layout.addWidget(self.sof_dir)
        sof_layout.setSpacing(10)
        sof_layout.addWidget(self.sof_status)

        # Terminal
        self.terminal_label = QLabel("Terminal")
        self.terminal_label.setStyleSheet(label_style)
        self.terminal = TerminalWidget()
        
        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addSpacing(10)
        main_layout.addWidget(self.emu_menu)
        main_layout.addSpacing(10)
        main_layout.addLayout(grid_layout)
        main_layout.addSpacing(10)
        main_layout.addLayout(settings_layout)
        main_layout.addSpacing(10)
        main_layout.addLayout(sof_layout)
        main_layout.addSpacing(30)
        main_layout.addWidget(self.terminal_label)
        main_layout.addWidget(self.terminal)
        self.setLayout(setWidgetBG(main_layout, panel_bg_color, 0, 0, 0, 0, outer_panel_border))
    
    def emulate(self):
        # Get emulation inputs
        update_status_and_progress('Emulating Chip Design')
        self.get_inputs()
        sof_exist = self.check_sof()
        
        if sof_exist:
            emulation_output = emulation_tool(self.cable, self.mode, self.device)
            self.terminal.terminal_output.setPlainText(emulation_output)
            
            if emulation_output != 'Check for improper connection and make sure the board is on.':
                update_status_and_progress('Emulation Complete', 'green')
            else:
                update_status_and_progress('Emulation Was Unsuccessful', 'red')
                
        else:
            self.terminal.terminal_output.setPlainText("SOF file does not exist. Make sure to create and compile the project.")  
            update_status_and_progress('Idle')
      
    def choose_file(self):
        update_status_and_progress('Setting Pin Assignments')
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "TCL Files (*.tcl)")
        if file_path:
            self.file_input.setText(file_path)
            pin_assignments(file_path)
            
        # Set pin assignments
        result = set_pin_assignments(file_path)  
        self.terminal.terminal_output.setPlainText(result)
        update_status_and_progress('Idle')
          
    def get_inputs(self):
        # Read values
        cable = self.cable_input.value() if self.cable_input.value() != 0 else 1  # default to 1 if 0
        mode = self.mode_input.text().strip() or "jtag"  # default to 'jtag' if empty
        device = self.device_input.value() if self.device_input.value() != 0 else 2  # default to 2 if 0
          
        # Assign back or store as needed
        self.cable = cable
        self.mode = mode
        self.device = device
        
    def check_sof(self):
        # Construct the path to the .sof file
        sof_path = f'{proj_config.get("PROJECT_DIRECTORY")}/output_files/{proj_config.get("TOP_LEVEL_ENTITY")}.sof'

        # Update the QLineEdit with the sof path
        self.sof_dir.setText(sof_path)

        # Check if the .sof file exists
        if os.path.exists(sof_path):
            self.sof_status.setText("Found")
            self.sof_status.setStyleSheet("color: green; border: none;")
            return True
        else:
            self.sof_status.setText("Not Found")
            self.sof_status.setStyleSheet("color: red; border: none;")
            return False
        
    def compile_project(self):
        update_status_and_progress('Compiling Project')
        self.run_task(compilation_tool, callback=self.on_compile_project_done)
    
    def on_compile_project_done(self, compilation_output):
        self.terminal.terminal_output.setPlainText(compilation_output[1])
        if compilation_output[0]:
            update_status_and_progress('Compilation Was Completed Successfully', color='green')
        else:
            update_status_and_progress('Compilation Was Unsuccessful', color='red')

        
    def display_waveform(self):
        update_status_and_progress('Displaying Waveform')
        self.run_task(ui_simulation_tool, callback=self.on_waveform_done)
    
    def on_waveform_done(self, simulation_output):
        self.terminal.terminal_output.setPlainText(simulation_output)
        update_status_and_progress('Idle')
        
    def on_error(self, message):
        create_msg_box(self, QMessageBox.Critical, "Error", f"Task failed: {message}")
        update_status_and_progress('Unsuccessful Operation', color='red')
        
    def run_task(self, task_fn, *args, callback=None ):
        worker = Worker(task_fn, *args)
        self.current_worker = worker

        def on_finished(result):
            if callback:
                callback(result)

        def on_error(error):
            self.on_error(error)

        worker.signals.finished.connect(on_finished)
        worker.signals.error.connect(on_error)
    
        self.threadpool.start(worker)

        
class GenerationMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QHBoxLayout()
        layout.setSpacing(10)  # Adjust spacing between buttons
        
        # Button Definitions
        self.gen_new_design = self.create_button(" Generate New Design", "icons/icons8-triangle-32.png")
        self.view_design = self.create_button(" View Design Code", "icons/research.png")
        self.view_tb = self.create_button("  View Testbench Code", "icons/research.png")
        self.stop_button = self.create_button("  Stop Process", "icons/icons8-stop.png")
        
        # Add buttons to layout
        layout.addWidget(self.gen_new_design)
        layout.addWidget(self.view_design)
        layout.addWidget(self.view_tb)
        layout.addWidget(self.stop_button)

        # Set layout
        self.setLayout(setWidgetBG(layout, 'white', -30, 0, -30, 0, border_radius = 5))

    def create_button(self, text, icon_path):
        button = QPushButton(text)
        button.setIcon(QIcon(icon_path))
        button.setStyleSheet(upper_menus_style)
        button.setIconSize(QSize(32, 32)) 
        return button

class DesignSpecification(QWidget):
    def __init__(self, parent=None, grandfather = None):
        super().__init__(parent)
        self.grandfather = grandfather
        self.threadpool = QThreadPool()
        self.current_worker = None
        self.init_ui()

    def init_ui(self):
        self.gen_menu = GenerationMenu()
        self.gen_menu.gen_new_design.clicked.connect(self.generate_design)
        self.gen_menu.view_design.clicked.connect(self.view_design)
        self.gen_menu.view_tb.clicked.connect(self.view_testbench)
        self.gen_menu.stop_button.clicked.connect(self.stop_process)

        # Labels
        self.module_name_label = QLabel("Module Name")
        self.module_name_label.setStyleSheet(label_style)
        self.module_desc_label = QLabel("Module Description")
        self.module_desc_label.setStyleSheet(label_style)
        self.driver_desc_label = QLabel("Driver Specifications")
        self.driver_desc_label.setStyleSheet(label_style)

        # Inputs
        self.module_name_input = QLineEdit()
        self.module_name_input.setStyleSheet(spec_input_style)
        self.module_desc_input = QTextEdit()
        self.module_desc_input.setStyleSheet(spec_input_style)
        self.driver_desc_input = QTextEdit()
        self.driver_desc_input.setStyleSheet(spec_input_style)

        # Layouts
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.module_name_label, 0, 0)
        grid_layout.addWidget(self.module_name_input, 0, 1)
        grid_layout.addWidget(self.module_desc_label, 1, 0)
        grid_layout.addWidget(self.module_desc_input, 1, 1)
        grid_layout.addWidget(self.driver_desc_label, 2, 0)
        grid_layout.addWidget(self.driver_desc_input, 2, 1)
        
        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addSpacing(20)
        main_layout.addWidget(self.gen_menu)
        main_layout.addSpacing(10)
        main_layout.addLayout(grid_layout)

        self.setLayout(setWidgetBG(main_layout, panel_bg_color, 0, 0, 0, 0, outer_panel_border))

    def enable_generate_button(self):
        self.gen_menu.gen_new_design.setDisabled(False)
        self.gen_menu.view_design.setDisabled(False)
        self.gen_menu.view_tb.setDisabled(False)
    
    def disable_generate_button(self):
        self.gen_menu.gen_new_design.setDisabled(True)
        self.gen_menu.view_design.setDisabled(True)
        self.gen_menu.view_tb.setDisabled(True)
        
    def get_filled_inputs(self):
        """
        Gathers text from text inputs only if they are not empty.
        Returns a dictionary of filled fields.
        """
        inputs = {
            "Module Name": self.module_name_input.text().strip(),
            "Module Description": self.module_desc_input.toPlainText().strip(),
            "Driver Specifications": self.driver_desc_input.toPlainText().strip(),
        }
        
        specs = (
            'Design Specifications:\n'
            f'Module Name: {inputs["Module Name"]}\n'
            f'Module Description: {inputs["Module Description"]}\n'
        )
        driver_specs = (
            f'{inputs["Driver Specifications"]}\n'
        )
        
        return specs, driver_specs

    def stop_process(self):
        if self.current_worker:
            self.current_worker.stop()
            self.enable_generate_button()

    def run_task(self, func, callback, *args):
        worker = Worker(func, *args)
        self.current_worker = worker
        worker.signals.finished.connect(callback)
        worker.signals.cancelled.connect(self.on_cancelled)
        worker.signals.error.connect(self.on_error)
        self.threadpool.start(worker)
        
    def generate_design(self):
        update_status_and_progress("Generating Design")
        self.disable_generate_button()
        self.specs , self.driver_specs = self.get_filled_inputs()
        args = [self.specs, self.driver_specs, config.feedback_cycles, config.universal_big_model, config.universal_small_model]
        
        self.run_task(ai_main, self.on_ai_main_done, *args)

    def on_error(self, message):
        self.enable_generate_button()
        QMessageBox.critical(self, "Error", f"Task failed: {message}")
        update_status_and_progress('Unsuccessful Operation', color='red')
      
    def on_cancelled(self):
        self.enable_generate_button()
        QMessageBox.information(self, "Cancelled", "The process was stopped.")
        update_status_and_progress('Operation Was Cancelled')

    def on_ai_main_done(self, result):
        if result != -1 :
            update_status_and_progress("Creating Testbench")
            self.run_task(create_testbench, self.on_testbench_done, result)
        else:
            self.enable_generate_button()
            QMessageBox.critical(self, "Error", f"Insecure prompt. Please check your inputs.")

    def on_testbench_done(self, result):
        update_status_and_progress("Compiling Project")
        self.run_task(complete_compilation_tool, self.on_compilation_done)

    def on_compilation_done(self, result):
        if result[0]:
            update_status_and_progress('Compilation Was Completed Successfully', color='green')
            self.enable_generate_button()
            create_msg_box(self, QMessageBox.Information, "Success", "Compilation was Completed Successfully")
        else:
            update_status_and_progress('Compilation Was Unsuccessful', color='red')
            self.enable_generate_button()
        
    def view_design(self):
        file_path = f'{proj_config.get("PROJECT_DIRECTORY")}/{proj_config.get("TOP_LEVEL_ENTITY")}.sv'
        self.open_code_editor(file_path)
    
    def view_testbench(self):
        file_path = f'{proj_config.get("PROJECT_DIRECTORY")}/{proj_config.get("TEST_BENCH_NAME")}.sv'
        self.open_code_editor(file_path)
    
    def open_code_editor(self, file_path):
        try:
            with open(file_path, 'r') as f:
                code = f.read()
                self.grandfather.code_widget.editor.setPlainText(code)
                self.grandfather.set_new_widget(self.grandfather.code_widget)
        except Exception as e:
            print(f"Error loading file: {e}")

class LLMSettings(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('LLM Settings')
        self.setMinimumWidth(700)
        grid_layout = QGridLayout()

        # API Key
        api_label = QLabel('API Key')
        api_label.setStyleSheet(label_style)
        self.api_input = QLineEdit()
        self.api_input.setStyleSheet(input_style)

        # Small model
        self.smname_label = QLabel("LLM Model Name (Small)")
        self.smname_label.setStyleSheet(label_style)
        self.smname_input = QLineEdit()
        self.smname_input.setPlaceholderText("Open AI LLM Model Name (This model is used for simple tasks, like processing input specifications.).")
        self.smname_input.setStyleSheet(input_style)

        # Big model
        self.bmname_label = QLabel("LLM Model Name (Big)")
        self.bmname_label.setStyleSheet(label_style)
        self.bmname_input = QLineEdit()
        self.bmname_input.setPlaceholderText("Open AI LLM Model Name (This model is used for complex major tasks, like generating chip design.).")
        self.bmname_input.setStyleSheet(input_style)

        # Add to grid (row, column)
        grid_layout.addWidget(api_label,      0, 0)
        grid_layout.addWidget(self.api_input, 0, 1)

        grid_layout.addWidget(self.smname_label,      1, 0)
        grid_layout.addWidget(self.smname_input,      1, 1)

        grid_layout.addWidget(self.bmname_label,      2, 0)
        grid_layout.addWidget(self.bmname_input,      2, 1)

        # Save button spanning two columns
        save_button = QPushButton('Save Settings')
        save_button.setStyleSheet(button_style)
        save_button.clicked.connect(self.save_settings)
        grid_layout.addWidget(save_button, 3, 0, 1, 2)

        self.setLayout(grid_layout)
        
        
    def save_settings(self):
        api_key = self.api_input.text().strip()
        if api_key:
            os.environ['OPENAI_API_KEY'] = api_key
            print(f"The new API key: {os.getenv('OPENAI_API_KEY')}")
        big_model = self.bmname_input.text().strip()
        small_model = self.smname_input.text().strip()
        
        if big_model in config.valid_llms:
            config.universal_big_model = big_model
            
        if small_model in config.valid_llms:
            config.universal_small_model = small_model
            
        print(f'Big LLM: {config.universal_big_model}')
        print(f'Small LLM: {config.universal_small_model}')
        
        create_msg_box(self, QMessageBox.Information, "Settings Saved", "LLM settings have been saved successfully.")

class PromptMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QHBoxLayout()
        layout.setSpacing(10)  # Adjust spacing between buttons
        
        # Button Definitions
        self.top_prompt = self.create_button("Top-Module Prompt")
        self.design_prompt = self.create_button("Chip Design Prompt")
        self.driver_prompt = self.create_button("Driver Design Prompt")
        self.validation_prompt = self.create_button("Validation Prompt")
        self.process_specs_prompt = self.create_button("Process Input Specifications Prompt")
        
        # Add buttons to layout
        
        layout.addWidget(self.top_prompt)
        layout.addWidget(self.design_prompt)
        layout.addWidget(self.driver_prompt)
        layout.addWidget(self.validation_prompt)
        layout.addWidget(self.process_specs_prompt)
        
        v_layout = QVBoxLayout()
        v_layout.addSpacing(5)
        v_layout.addLayout(layout)
        v_layout.addSpacing(5)

        # Set layout
        self.setLayout(setWidgetBG(v_layout, prompt_menu_bg , -30, 0, -30, 0, border_radius = 5))

    def create_button(self, text):
        button = QPushButton(text)
        button.setStyleSheet(home_menu_style)
        return button

class EditPrompts(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Edit System Prompts')
        self.setMinimumSize(1200, 800)
        self.setStyleSheet('background-color:white;')
        
        self.current_prompt_id = 0
        self.prompt_menu = PromptMenu(self)
        self.prompt_menu.top_prompt.clicked.connect(self.on_top_click)  
        self.prompt_menu.design_prompt.clicked.connect(self.on_design_click)
        self.prompt_menu.driver_prompt.clicked.connect(self.on_driver_click)
        self.prompt_menu.validation_prompt.clicked.connect(self.on_validation_click)
        self.prompt_menu.process_specs_prompt.clicked.connect(self.on_process_specs_click)
        self.prompt_txt_area = QTextEdit()
        self.prompt_txt_area.setStyleSheet(spec_input_style)
        self.prompt_txt_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        '''buttons_layout = QHBoxLayout()
        self.save_prompts_btn = QPushButton('Save Prompts')
        self.restore_prompts_btn = QPushButton('Restore Default Prompts')
        self.save_prompts_btn.setStyleSheet(save_button_style)
        self.restore_prompts_btn.setStyleSheet(restore_button_style)
        self.save_prompts_btn.clicked.connect(self.save_prompts)
        self.restore_prompts_btn.clicked.connect(self.restore_prompts)
        buttons_layout.addWidget(self.save_prompts_btn)
        buttons_layout.addWidget(self.restore_prompts_btn)'''
        
        buttons_layout = QGridLayout()

        # Create buttons
        self.save_prompts_btn = QPushButton('Save Prompts')
        self.restore_prompts_btn = QPushButton('Restore Default Prompts')

        self.save_prompts_btn.setFixedWidth(300)
        self.restore_prompts_btn.setFixedWidth(300)

        # Apply styles
        self.save_prompts_btn.setStyleSheet(save_button_style)
        self.restore_prompts_btn.setStyleSheet(restore_button_style)

        # Connect signals
        self.save_prompts_btn.clicked.connect(self.save_prompts)
        self.restore_prompts_btn.clicked.connect(self.restore_prompts)

        # Add spacers and buttons to the grid: row 0, columns 0–4
        buttons_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 0, 0)
        buttons_layout.addWidget(self.save_prompts_btn, 0, 1)
        buttons_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum), 0, 2)
        buttons_layout.addWidget(self.restore_prompts_btn, 0, 3)
        buttons_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 0, 4)

        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.prompt_menu)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.prompt_txt_area)
        main_layout.addSpacing(10)
        main_layout.addLayout(buttons_layout)
        
        self.setLayout(main_layout)
        
    def restore_prompts(self):
        session.db_obj.delete_customized_prompts(session.current_user.user_id)
        session.current_prompts['top_prompt'] = session.db_obj.get_default_prompt_by_id(101)['prompt']
        session.current_prompts['design_prompt'] = session.db_obj.get_default_prompt_by_id(103)['prompt']
        session.current_prompts['driver_prompt'] = session.db_obj.get_default_prompt_by_id(102)['prompt']
        session.current_prompts['validation_prompt'] = session.db_obj.get_default_prompt_by_id(104)['prompt']
        session.current_prompts['process_specs_prompt'] = session.db_obj.get_default_prompt_by_id(105)['prompt']
        
        create_msg_box(self, QMessageBox.Information, 'Default Prompts Restored', 'The default system prompts have been restored.')


    def save_prompts(self):
        edited_prompt = self.prompt_txt_area.toPlainText()
        print(f'Edited prompt ID: {self.current_prompt_id}\nNew prompt: {edited_prompt}')
        if self.current_prompt_id == 101:
            session.current_prompts['top_prompt'] = edited_prompt
        elif self.current_prompt_id == 102:
            session.current_prompts['driver_prompt'] = edited_prompt
        elif self.current_prompt_id == 103:
            session.current_prompts['design_prompt'] = edited_prompt
        elif self.current_prompt_id == 104:
            session.current_prompts['validation_prompt'] = edited_prompt
        elif self.current_prompt_id == 105:
            session.current_prompts['process_specs_prompt'] = edited_prompt
            

        session.db_obj.save_customized_prompts(session.current_prompts, session.current_user.user_id)
        create_msg_box(self, QMessageBox.Information, 'Prompt Saved', 'Your changes have been saved successfully. The default system prompt has been overridden.')


    def on_top_click(self):
        self.show_prompt(101, 'top_prompt')

    def on_driver_click(self):
        self.show_prompt(102, 'driver_prompt')
        
    def on_design_click(self):
        self.show_prompt(103, 'design_prompt')
        
    def on_validation_click(self):
        self.show_prompt(104, 'validation_prompt')
    
    def on_process_specs_click(self):
        self.show_prompt(105, 'process_specs_prompt')
        
    def show_prompt(self,prompt_id, prompt_name):
        if session.current_prompts:
            self.current_prompt_id = prompt_id
            self.prompt_txt_area.setText(session.current_prompts[prompt_name])
              
class GridWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Create grid layout
        self.grid_layout = QGridLayout()
        self.grid_layout.setVerticalSpacing(15)
        
        # --- First Row: Status Label, Empty Space, Empty Space, Progress Bar (spanning 2 columns) ---
        self.status_label = QLabel("Status: In Progress")
        #self.progress_bar = QProgressBar()
        
        self.status_label.setStyleSheet(status_style) 
        self.status_label.setFixedSize(400, 30) 
        self.status_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        #self.progress_bar.setValue(0)
        #self.progress_bar.setStyleSheet(bar_style_before)
        #self.progress_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        register_ui(self.status_label)
        
        self.grid_layout.addWidget(self.status_label, 0, 0)  
        self.grid_layout.setColumnStretch(1,1)
        #self.add_button(self.grid_layout, " Chat History", QSize(27, 27), self.show_prompt_dialog, "icons/chat.png", 0,2)
        self.add_button(self.grid_layout, " Edit System Prompts", QSize(26, 26), self.show_prompt_dialog, "icons/computer.png",0,3)
        self.add_button(self.grid_layout, " Settings", QSize(23, 23), self.show_settings_dialog, "icons/settings.png",0,4)
        
        # --- Second Row: Expanding Widget Placeholder ---
        self.custom_widget = QLabel("Placeholder Widget")  
        self.custom_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.grid_layout.addWidget(self.custom_widget, 1, 0, 1, 5)  
        
        # --- Last Row: Previous & Next Buttons ---
        self.prev_button = QPushButton("Previous")
        self.next_button = QPushButton("Next")
        self.prev_button.setFixedSize(100, 40)
        self.next_button.setFixedSize(100, 40)
        self.prev_button.setStyleSheet(button_style)
        self.next_button.setStyleSheet(button_style)
        # Button Actions
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button.clicked.connect(self.next_page)
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)  
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)
        self.grid_layout.addLayout(button_layout, 2, 0, 1, 5)  
        
        # Page System
        #self.project_widget = ProjectSetup(parent=self)
        #self.project_widget.hide()
        self.design_widget = DesignSpecification(parent=self, grandfather=parent)
        self.design_widget.hide()
        self.emulation_widget = Emulation(parent=self)
        self.emulation_widget.hide()
        self.pages = [ self.design_widget,self.emulation_widget]

        self.current_page = 0
        self.update_buttons()
        self.set_custom_widget(self.pages[self.current_page])

        # Create a main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.grid_layout)
        self.setLayout(main_layout)
        
    def add_button(self, layout, tool_tip_text, icon_size , function, icon_dir, row, col):
        """Helper function to add a menu button"""
        button = QPushButton()
        button.setToolTip(tool_tip_text)
        button.setText(tool_tip_text)
        button.setIcon(QIcon(icon_dir)) 
        button.setIconSize(icon_size) 
        button.setStyleSheet(grid_btn_style)
        button.clicked.connect(function)
        layout.addWidget(button, row, col)
        
    def show_prompt_dialog(self):
        dialog = EditPrompts(self)
        dialog.exec_()
    
    def show_settings_dialog(self):
        dialog = LLMSettings(self)
        dialog.exec_()  
        
    def set_custom_widget(self, new_widget):
        """Replace the second-row widget dynamically while ensuring proper deletion."""
        if self.custom_widget is not None:  
            self.custom_widget.hide()  # Remove the old widget
    
        self.custom_widget = new_widget  # Store the new widget
        self.custom_widget.show()  # Store the new widget
        self.custom_widget.setParent(self)  # Ensure it's properly parented
        self.custom_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.grid_layout.addWidget(self.custom_widget, 1, 0, 1, 5)
        self.custom_widget.show()

    def next_page(self):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self.set_custom_widget(self.pages[self.current_page])
            self.update_buttons()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.set_custom_widget(self.pages[self.current_page])
            self.update_buttons()

    def update_buttons(self):
        """Enable/Disable buttons based on the current page."""
        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(self.current_page < len(self.pages) - 1)











		 
			  
	 