class ProjectConfig:
    def __init__(self):   
        """Initialize default configuration values."""
        self.QUARTUS_DIRECTORY = "D:/NewQuartus/installDir/intelFPGA_lite/23.1std/quartus"
        self.PROJECT_DIRECTORY = ""
        self.PROJECT_NAME = ""
        self.TOP_LEVEL_ENTITY = ""
        self.BOARD = "DE1-SoC Board"
        self.EDA_SIMULATION_TOOL = "Questa Intel FPGA (SystemVerilog)"
        self.EDA_OUTPUT_DATA_FORMAT = "SYSTEMVERILOG HDL"
        self.HDL_LANGUAGE = ""
        
        self.TEST_BENCH_NAME = ""
        self.PROJECT_QUESTA_DIRECTORY = "/simulation/questa"
        self.NATIVELINK_DIRECTORY = self.QUARTUS_DIRECTORY + "/common/tcl/internal/nativelink/qnativesim.tcl"
        self.OUTPUT_FILES_DIRECTORY = "/output_files"
        #self.TEMP_DIRECTORY = "D:/NewQuartus/temp"
        self.TEMP_DIRECTORY = "C:/Users/hp/OneDrive/Desktop/SDV/temp"

        # Scripts
        self.scripts = {
            "quartus_script_project_settings": """ 
# Environment variables
set proj_dir "{PROJECT_DIRECTORY}"

# Create directory if it doesn't exist
if {{![file isdirectory $proj_dir]}} {{
    file mkdir $proj_dir
}}

# Change to the project directory
cd $proj_dir

# To create a new project
project_new {PROJECT_NAME} -overwrite -revision {PROJECT_NAME}

# Project settings
set_global_assignment -name FAMILY "Cyclone V"
set_global_assignment -name DEVICE 5CSEMA5F31C6
set_global_assignment -name TOP_LEVEL_ENTITY {TOP_LEVEL_ENTITY}
set_global_assignment -name PROJECT_OUTPUT_DIRECTORY output_files
set_global_assignment -name BOARD "{BOARD}"

# EDA Tools
set_global_assignment -name EDA_SIMULATION_TOOL "{EDA_SIMULATION_TOOL}"
set_global_assignment -name EDA_OUTPUT_DATA_FORMAT "{EDA_OUTPUT_DATA_FORMAT}" -section_id eda_simulation
set_global_assignment -name EDA_GENERATE_FUNCTIONAL_NETLIST OFF -section_id eda_board_design_timing
set_global_assignment -name EDA_GENERATE_FUNCTIONAL_NETLIST OFF -section_id eda_board_design_symbol
set_global_assignment -name EDA_GENERATE_FUNCTIONAL_NETLIST OFF -section_id eda_board_design_signal_integrity
set_global_assignment -name EDA_GENERATE_FUNCTIONAL_NETLIST OFF -section_id eda_board_design_boundary_scan

# Testbench
set_global_assignment -name SYSTEMVERILOG_FILE {TEST_BENCH_NAME}.sv
set_global_assignment -name EDA_DESIGN_INSTANCE_NAME NA -section_id {TEST_BENCH_NAME}
set_global_assignment -name EDA_TEST_BENCH_MODULE_NAME {TEST_BENCH_NAME} -section_id {TEST_BENCH_NAME}
set_global_assignment -name EDA_TEST_BENCH_FILE {TEST_BENCH_NAME}.sv -section_id {TEST_BENCH_NAME}
set_global_assignment -name EDA_TIME_SCALE "1 ps" -section_id eda_simulation
set_global_assignment -name EDA_TEST_BENCH_ENABLE_STATUS TEST_BENCH_MODE -section_id eda_simulation
set_global_assignment -name EDA_NATIVELINK_SIMULATION_TEST_BENCH {TEST_BENCH_NAME} -section_id eda_simulation
set_global_assignment -name EDA_TEST_BENCH_NAME {TEST_BENCH_NAME} -section_id eda_simulation

set_global_assignment  -name PHYSICAL_SYNTHESIS_EFFORT FAST
set_global_assignment  -name FITTER_EFFORT FAST_FIT

project_close
""",
            "quartus_script_project_compilation": """
project_open {PROJECT_DIRECTORY}/{PROJECT_NAME}

load_package flow

execute_flow -compile

project_close
""",
            "quartus_script_temp_project_settings": """ 
# Environment variables
set proj_dir "{TEMP_DIRECTORY}/{PROJECT_NAME}"

# Create directory if it doesn't exist
if {{![file isdirectory $proj_dir]}} {{
    file mkdir $proj_dir
}}

# Change to the project directory
cd $proj_dir

# To create a new project
project_new {PROJECT_NAME} -overwrite -revision {PROJECT_NAME}

# Project settings
set_global_assignment -name FAMILY "Cyclone V"
set_global_assignment -name DEVICE 5CSEMA5F31C6
set_global_assignment -name TOP_LEVEL_ENTITY {TOP_LEVEL_ENTITY}
set_global_assignment -name PROJECT_OUTPUT_DIRECTORY output_files
set_global_assignment -name BOARD "{BOARD}"

# EDA Tools
set_global_assignment -name EDA_SIMULATION_TOOL "{EDA_SIMULATION_TOOL}"
set_global_assignment -name EDA_OUTPUT_DATA_FORMAT "{EDA_OUTPUT_DATA_FORMAT}" -section_id eda_simulation
set_global_assignment -name EDA_TIME_SCALE "1 ps" -section_id eda_simulation
set_global_assignment -name EDA_GENERATE_FUNCTIONAL_NETLIST OFF -section_id eda_board_design_timing
set_global_assignment -name EDA_GENERATE_FUNCTIONAL_NETLIST OFF -section_id eda_board_design_symbol
set_global_assignment -name EDA_GENERATE_FUNCTIONAL_NETLIST OFF -section_id eda_board_design_signal_integrity
set_global_assignment -name EDA_GENERATE_FUNCTIONAL_NETLIST OFF -section_id eda_board_design_boundary_scan

project_close
""",
            "quartus_script_temp_project_compilation": """
project_open {TEMP_DIRECTORY}/{PROJECT_NAME}/{PROJECT_NAME}

load_package flow

execute_module -tool map

project_close
"""
        }
        
        self.list_of_scripts = ["quartus_script_project_compilation", 
                                "quartus_script_temp_project_compilation",
                                "quartus_script_project_settings", 
                                "quartus_script_temp_project_settings"]


    def _generate_script(self, script_name):
        """Generate a Quartus script based on current settings."""
        if script_name in self.scripts:
            return self.scripts[script_name].format(
                PROJECT_DIRECTORY=self.PROJECT_DIRECTORY,
                PROJECT_NAME=self.PROJECT_NAME,
                TOP_LEVEL_ENTITY=self.TOP_LEVEL_ENTITY,
                BOARD=self.BOARD,
                EDA_SIMULATION_TOOL=self.EDA_SIMULATION_TOOL,
                EDA_OUTPUT_DATA_FORMAT=self.EDA_OUTPUT_DATA_FORMAT,
                TEST_BENCH_NAME=self.TEST_BENCH_NAME,
                TEMP_DIRECTORY = self.TEMP_DIRECTORY
            )
        return None

    def _generate_report_files(self):
        """Generate the list of report files based on project configuration."""
        return [
            f"{self.PROJECT_DIRECTORY}{self.OUTPUT_FILES_DIRECTORY}/{self.PROJECT_NAME}.map.rpt",
            #f"{self.PROJECT_DIRECTORY}{self.OUTPUT_FILES_DIRECTORY}/{self.PROJECT_NAME}.sta.rpt",
            #f"{self.PROJECT_DIRECTORY}{self.OUTPUT_FILES_DIRECTORY}/{self.PROJECT_NAME}.asm.rpt",
            #f"{self.PROJECT_DIRECTORY}{self.OUTPUT_FILES_DIRECTORY}/{self.PROJECT_NAME}.eda.rpt",
            #f"{self.PROJECT_DIRECTORY}{self.OUTPUT_FILES_DIRECTORY}/{self.PROJECT_NAME}.fit.rpt",
        ]

    # Getter
    def get(self, key):
        """Retrieve a configuration value or dynamically generated data."""
        if key in self.list_of_scripts:
            return self._generate_script(key)
        elif key == "REPORT_FILES":
            return self._generate_report_files()
        elif key == "PROJECT_QUESTA_DIRECTORY":
            return f"{self.PROJECT_DIRECTORY}{self.PROJECT_QUESTA_DIRECTORY}"
        elif key == "OUTPUT_FILES_DIRECTORY":
            return f"{self.PROJECT_DIRECTORY}{self.OUTPUT_FILES_DIRECTORY}"
        return getattr(self, key, None)

    # Setter
    def set(self, key, value):
        """Set a configuration value."""
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError(f"Invalid configuration key: {key}")

