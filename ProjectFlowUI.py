from Imports import *
import time
from DataClasses import *

# Mock long-running functions with stop check
'''def ai_main_fake(worker, specs):
    print("ai_main_fake called with:", specs)
    for _ in range(4):
        if worker.is_stopped():
            return None
        time.sleep(0.5)
    return {"signals": ["clk", "reset"]}

def create_testbench(worker, signals):
    print("create_testbench called with:", signals)
    for _ in range(4):
        if worker.is_stopped():
            return None
        time.sleep(0.5)
    return {"tb": "testbench_code"}

def complete_compilation_tool(worker):
    print("complete_compilation_tool called with: no arguments")
    for _ in range(4):
        if worker.is_stopped():
            return None
        time.sleep(0.5)
    return "Compilation Success"
'''

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
        self.cable_input.setStyleSheet(spinbox_style)
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
        self.device_input.setStyleSheet(spinbox_style)
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
        self.setLayout(setWidgetBG(main_layout, panel_bg_color, 0, 0, 0, 0, panel_border))
    
    def emulate(self):
        # Get emulation inputs
        update_status_and_progress('Emulating Chip Design')
        self.get_inputs()
        sof_exist = self.check_sof()
        
        if sof_exist:
            emulation_output = emulation_tool(self.cable, self.mode, self.device)
            self.terminal.terminal_output.setPlainText(emulation_output)
            update_status_and_progress('Emulation Complete', 100)
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
        update_status_and_progress('Idle', 90)
          
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
        
    '''def compile_project(self):
        update_status_and_progress('Compiling Project')
        compilation_output = complete_compilation_tool()
        self.terminal.terminal_output.setPlainText(compilation_output)
        update_status_and_progress('Idle')'''
        
    def compile_project(self):
        update_status_and_progress('Compiling Project')
        self.run_task(complete_compilation_tool(), self.on_compile_project_done)
    
    def on_compile_project_done(self, compilation_output):
        self.terminal.terminal_output.setPlainText(compilation_output)
        update_status_and_progress('Compiling Completed Successfully')
        
    def display_waveform(self):
        update_status_and_progress('Displaying Waveform')
        self.run_task(ui_simulation_tool(), self.on_waveform_done)
    
    def on_waveform_done(self, simulation_output):
        self.terminal.terminal_output.setPlainText(simulation_output)
        update_status_and_progress('Idle')
        
    def on_error(self, message):
        create_msg_box(self, QMessageBox.critical, "Error", f"Task failed: {message}")
        
    def run_task(self, task_fn, callback=None, *args):
        print("Setting up worker for", task_fn.__name__)
        worker = Worker(task_fn, *args)
        self.current_worker = worker

        def on_finished(result):
            print("Worker finished with result:", result)
            if callback:
                callback(result)

        def on_error(error):
            print("Worker error:", error)
            self.on_error(error)

        worker.signals.finished.connect(on_finished)
        worker.signals.error.connect(on_error)
    
        self.threadpool.start(worker)
        print("Worker started.")
        
class GenerationMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QHBoxLayout()
        layout.setSpacing(10)  # Adjust spacing between buttons
        
        # Button Definitions
        self.gen_new_design = self.create_button(" Generate New Design", "icons/gennew.png")
        self.view_design = self.create_button(" View Design Code", "icons/viewd.png")
        self.view_tb = self.create_button("  View Testbench Code", "icons/viewt.png")
        self.stop_button = self.create_button("  Stop Process", "icons/viewt.png")
        
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
        self.io_label = QLabel("Inputs/Outputs")
        self.io_label.setStyleSheet(label_style)
        self.errors_label = QLabel("Errors and Edits")
        self.errors_label.setStyleSheet(label_style)

        # Inputs
        self.module_name_input = QLineEdit()
        self.module_name_input.setStyleSheet(spec_input_style)
        self.module_desc_input = QTextEdit()
        self.module_desc_input.setStyleSheet(spec_input_style)
        self.io_input = QTextEdit()
        self.io_input.setStyleSheet(spec_input_style)
        self.errors_input = QTextEdit()
        self.errors_input.setStyleSheet(spec_input_style)

        # Layouts
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.module_name_label, 0, 0)
        grid_layout.addWidget(self.module_name_input, 0, 1)
        grid_layout.addWidget(self.module_desc_label, 1, 0)
        grid_layout.addWidget(self.module_desc_input, 1, 1)
        grid_layout.addWidget(self.io_label, 2, 0)
        grid_layout.addWidget(self.io_input, 2, 1)
        grid_layout.addWidget(self.errors_label, 3, 0)
        grid_layout.addWidget(self.errors_input, 3, 1)
        
        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addSpacing(20)
        main_layout.addWidget(self.gen_menu)
        main_layout.addSpacing(10)
        main_layout.addLayout(grid_layout)

        self.setLayout(setWidgetBG(main_layout, panel_bg_color, 0, 0, 0, 0, panel_border))

    def enable_generate_button(self):
        self.gen_menu.gen_new_design.setDisabled(False)
    
    def disable_generate_button(self):
        self.gen_menu.gen_new_design.setDisabled(True)
        
    def get_filled_inputs(self):
        """
        Gathers text from text inputs only if they are not empty.
        Returns a dictionary of filled fields.
        """
        inputs = {
            "Module Name": self.module_name_input.text().strip(),
            "Module Description": self.module_desc_input.toPlainText().strip(),
            "Inputs/Outputs": self.io_input.toPlainText().strip(),
            "Errors and Edits": self.errors_input.toPlainText().strip()
        }
        
        specs = 'Design Specifications:\n'

        for key, value in inputs.items():
                specs += f'{key}:\n{value}\n'

        return specs

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
        self.specs = self.get_filled_inputs()
        
        self.run_task(ai_main, self.on_ai_main_done, self.specs)

    def on_error(self, message):
        self.enable_generate_button()
        QMessageBox.critical(self, "Error", f"Task failed: {message}")
      
    def on_cancelled(self):
        self.enable_generate_button()
        QMessageBox.information(self, "Cancelled", "The process was stopped.")

    def on_ai_main_done(self, result):
        if result != -1 :
            update_status_and_progress("Creating Testbench", 40)
            self.run_task(create_testbench, self.on_testbench_done, result)
            print("tb result:   ", result)
        else:
            self.enable_generate_button()
            QMessageBox.critical(self, "Error", f"Insecure prompt. Please check your inputs.")

    def on_testbench_done(self, result):
        update_status_and_progress("Compiling Project", 55)
        self.run_task(complete_compilation_tool, self.on_compilation_done)

    def on_compilation_done(self, result):
        update_status_and_progress("Compilation Completed", 65)
        self.enable_generate_button()
        QMessageBox.information(self, "Success", "Compilation was Completed Successfully.")
        

    ''''def _run_design_pipeline(self, specs):
        try:
            signals = ai_main(specs, feedback_cycles = feedback_cycles)
            if signals == -1:
                return "fail:Insecure prompt. Please check your inputs."
            update_status_and_progress("Creating Testbench", 40)
            create_testbench(signals)
            update_status_and_progress("Compiling Project", 55)
            complete_compilation_tool()
            update_status_and_progress("Compilation Completed", 65)
            return "success:Process completed. Check your code for relevance."
        except Exception as e:
            return f"fail:{str(e)}"

    def _check_future(self, future):
        if future.done():
            self.timer.stop()
            result = future.result()
            if result.startswith("success:"):
                QMessageBox.information(self, "Success", result.split(":", 1)[1])
            else:
                QMessageBox.critical(self, "Error", result.split(":", 1)[1])'''

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

class ProjectSetup(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        # Grid Layout for Inputs
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        # Directory Selection
        self.dir_label = QLabel("Project Directory:")
        self.dir_label.setStyleSheet(label_style)

        self.dir_input = QLineEdit()
        self.dir_input.setPlaceholderText("Select project directory")
        self.dir_input.setStyleSheet(input_style)

        self.browse_button = QPushButton("Browse")
        self.browse_button.setStyleSheet(button_style)
        self.browse_button.clicked.connect(self.browse_directory)

        grid_layout.addWidget(self.dir_label, 0, 0)
        grid_layout.addWidget(self.dir_input, 0, 1)
        grid_layout.addWidget(self.browse_button, 0, 2)

        # Project Name
        self.pname_label = QLabel("Project Name:")
        self.pname_label.setStyleSheet(label_style)

        self.pname_input = QLineEdit()
        self.pname_input.setPlaceholderText("No illegal characters like -")
        self.pname_input.setStyleSheet(input_style)

        grid_layout.addWidget(self.pname_label, 1, 0)
        grid_layout.addWidget(self.pname_input, 1, 1, 1, 2)

        # Top-Level Module Name
        self.tname_label = QLabel("Top-Level Module Name:")
        self.tname_label.setStyleSheet(label_style)

        self.tname_input = QLineEdit()
        self.tname_input.setPlaceholderText("No illegal characters like -")
        self.tname_input.setStyleSheet(input_style)

        grid_layout.addWidget(self.tname_label, 2, 0)
        grid_layout.addWidget(self.tname_input, 2, 1, 1, 2)
        
        # Testbench Module Name
        self.tbname_label = QLabel("Testbench Name:")
        self.tbname_label.setStyleSheet(label_style)

        self.tbname_input = QLineEdit()
        self.tbname_input.setPlaceholderText("No illegal characters like -")
        self.tbname_input.setStyleSheet(input_style)

        grid_layout.addWidget(self.tbname_label, 3, 0)
        grid_layout.addWidget(self.tbname_input, 3, 1, 1, 2)

        # HDL Language Selection
        self.hdl_label = QLabel("HDL Language:")
        self.hdl_label.setStyleSheet(label_style)

        self.hdl_combobox = QComboBox()
        self.hdl_combobox.addItems(["SystemVerilog", "Verilog", "VHDL"])
        self.hdl_combobox.setStyleSheet(combobox_style)

        grid_layout.addWidget(self.hdl_label, 4, 0)
        grid_layout.addWidget(self.hdl_combobox, 4, 1, 1, 2)
        
        # Simulation Tool Selection
        self.sim_label = QLabel("Simulation Tool:")
        self.sim_label.setStyleSheet(label_style)

        self.sim_combobox = QComboBox()
        self.sim_combobox.addItems(simulation_tools)
        self.sim_combobox.setStyleSheet(combobox_style)

        grid_layout.addWidget(self.sim_label, 5, 0)
        grid_layout.addWidget(self.sim_combobox, 5, 1, 1, 2)
        

        # EDA Data Selection
        self.eda_format_label = QLabel("EDA Output Data Format:")
        self.eda_format_label.setStyleSheet(label_style)

        self.eda_format_combobox = QComboBox()
        self.eda_format_combobox.addItems(eda_output_data_formats) 
        self.eda_format_combobox.setStyleSheet(combobox_style)

        grid_layout.addWidget(self.eda_format_label, 6, 0)
        grid_layout.addWidget(self.eda_format_combobox, 6, 1, 1, 2)
        
        
        # Board Selection
        self.board_label = QLabel("FPGA Board:")
        self.board_label.setStyleSheet(label_style)

        self.board_combobox = QComboBox()
        self.board_combobox.addItems(fpga_boards) 
        self.board_combobox.setStyleSheet(combobox_style)

        grid_layout.addWidget(self.board_label, 7, 0)
        grid_layout.addWidget(self.board_combobox, 7, 1, 1, 2)


        # Small and Big Models
        self.smname_label = QLabel("LLM Model Name (Small)")
        self.smname_label.setStyleSheet(label_style)
        self.bmname_label = QLabel("LLM Model Name (Big)")
        self.bmname_label.setStyleSheet(label_style)

        self.smname_input = QLineEdit()
        self.smname_input.setPlaceholderText("Open AI LLM Model Name (This model is used for simple tasks, like processing input specifications.).")
        self.smname_input.setStyleSheet(input_style)
        self.bmname_input = QLineEdit()
        self.bmname_input.setPlaceholderText("Open AI LLM Model Name (This model is used for complex major tasks, like generating chip design.).")
        self.bmname_input.setStyleSheet(input_style)
        
        grid_layout.addWidget(self.smname_label, 8, 0)
        grid_layout.addWidget(self.smname_input, 8, 1, 1, 2)
        grid_layout.addWidget(self.bmname_label, 9, 0)
        grid_layout.addWidget(self.bmname_input, 9, 1, 1, 2)
        
        # Feedback cycles
        self.feed_label = QLabel("Feedback cycles:")
        self.feed_label.setStyleSheet(label_style)

        self.feed_spin = QSpinBox()
        self.feed_spin.setStyleSheet(spinbox_style)

        grid_layout.addWidget(self.feed_label, 10, 0)
        grid_layout.addWidget(self.feed_spin, 10, 1, 1, 2)
        
        self.save_button = QPushButton("Save project settings")
        self.save_button.setStyleSheet(button_style)
        self.save_button.clicked.connect(self.save_settings)
        self.save_button.setFixedWidth(200)
        self.save_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        save_layout = QHBoxLayout()
        save_layout.addWidget(self.save_button)

        layout.addStretch()
        layout.addStretch()
        layout.addLayout(grid_layout)
        layout.addStretch()
        layout.addLayout(save_layout)
        layout.addStretch()
        layout.addStretch()
        layout.addStretch()
        

        self.setLayout(setWidgetBG(layout, panel_bg_color, 0, 0, 0, 0, panel_border))

    
    def browse_directory(self):
        """Open a directory selection dialog."""
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.dir_input.setText(directory)
        
    def save_settings(self):
        update_status_and_progress('Saving Project Settings')
        # Check for an empty project directory
        project_dir = self.dir_input.text().strip()
        if not project_dir:
            create_msg_box(self, QMessageBox.Warning, "Input Error",  "Project directory cannot be empty.")
            return

        # Define a regex pattern for valid names: 
        # - Starts with a letter or underscore
        # - Contains only letters, digits, underscores, and dollar signs
        valid_name_pattern = r"^[a-zA-Z_][a-zA-Z0-9_$]*$"

        def is_valid_name(name):
            return re.fullmatch(valid_name_pattern, name) is not None

        # Retrieve text from input fields
        project_name = self.pname_input.text().strip()
        module_name = self.tname_input.text().strip()
        testbench_name = self.tbname_input.text().strip()
        
        if module_name == testbench_name:
            QMessageBox.warning(self, "Invalid Input", "Top-Level and Testbench modules have the same names")
            return

        # Validate names
        if not is_valid_name(project_name):
            QMessageBox.warning(self, "Invalid Input", "Project name must start with a letter or underscore and contain only letters, digits, underscores, or dollar signs.")
            return
        if not is_valid_name(module_name):
            QMessageBox.warning(self, "Invalid Input", "Module name must start with a letter or underscore and contain only letters, digits, underscores, or dollar signs.")
            return
        if not is_valid_name(testbench_name):
            QMessageBox.warning(self, "Invalid Input", "Testbench name must start with a letter or underscore and contain only letters, digits, underscores, or dollar signs.")
            return
        

        # Assign simulation tool, models, and HDL language
        selected_hdl = self.hdl_combobox.currentText()
        selected_sim_tool = self.sim_combobox.currentText()
        selected_eda = self.eda_format_combobox.currentText()
        selected_board = self.board_combobox.currentText()
        global feedback_cycles
        feedback_cycles = self.feed_spin.value() if self.feed_spin.value() != 0 else 3
        print("feedback_cycles  ", feedback_cycles)
        
        # Store settings
        self.settings = {
            "PROJECT_DIRECTORY": project_dir,
            "PROJECT_NAME": project_name,
            "TOP_LEVEL_ENTITY": module_name,
            "TEST_BENCH_NAME": testbench_name,
            "HDL_LANGUAGE": selected_hdl,
            "EDA_SIMULATION_TOOL": selected_sim_tool,
            "EDA_OUTPUT_DATA_FORMAT": selected_eda,
            "BOARD": selected_board
        }    
        
        for key, value in self.settings.items():
                    proj_config.set(key, value)
                    
        new_project = Project(
            project_name=project_name,
            project_directory=project_dir,
            no_api_calls=3,
            top_module_name=module_name,
            testbench_name=testbench_name,
            board=selected_board,
            eda_output_format=selected_eda,
            simulation_tool=selected_sim_tool,
            feedback_cycles=2,
            hdl=selected_hdl,
            editors=""
        )
        
        db_obj.insert_project(new_project)
                    
        QMessageBox.information(self, "Success", "Settings saved successfully!")
        update_status_and_progress('Idle', 15)
                
        
class GridWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Create grid layout
        self.grid_layout = QGridLayout()
        self.grid_layout.setVerticalSpacing(15)
        
        # --- First Row: Status Label, Empty Space, Empty Space, Progress Bar (spanning 2 columns) ---
        self.status_label = QLabel("Status: In Progress")
        self.progress_bar = QProgressBar()
        
        self.status_label.setStyleSheet(status_style) 
        self.status_label.setFixedSize(400, 30) 
        self.status_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet(bar_style_before)
        self.progress_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        register_ui(self.status_label, self.progress_bar)
        
        self.grid_layout.addWidget(self.status_label, 0, 0)  
        self.grid_layout.setColumnStretch(1, 1)  
        self.grid_layout.setColumnStretch(2, 1)
        self.grid_layout.addWidget(self.progress_bar, 0, 2, 1, 2) 
        
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
        self.project_widget = ProjectSetup(parent=self)
        self.project_widget.hide()
        self.design_widget = DesignSpecification(parent=self, grandfather=parent)
        self.design_widget.hide()
        self.emulation_widget = Emulation(parent=self)
        self.emulation_widget.hide()
        self.pages = [self.project_widget, self.design_widget,self.emulation_widget]

        self.current_page = 0
        self.update_buttons()
        self.set_custom_widget(self.pages[self.current_page])

        # Create a main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.grid_layout)
        self.setLayout(main_layout)
        

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

    def update_style(self, value):
        """Update the font color based on progress value."""
        if value >= 50:
            self.progress_bar.setStyleSheet(bar_style_after)  # Change font color
        else:
            self.progress_bar.setStyleSheet(bar_style_before)  # Default color

    #def stop_current_task(self):