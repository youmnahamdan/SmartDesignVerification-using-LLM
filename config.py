# config.py
from ProjectConfig import ProjectConfig  # Adjust this import if needed

# Initialize once and share across modules
proj_config = ProjectConfig()
temp_proj_config = ProjectConfig()

# EDA Output Data Formats
eda_output_data_formats = ["SYSTEMVERILOG HDL"]
fpga_boards = ["DE1-SoC Board"]
simulation_tools = ["Questa Intel FPGA (SystemVerilog)"]
DB_NAME = "SDV.db"