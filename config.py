# config.py
from ProjectConfig import ProjectConfig  # Adjust this import if needed
from concurrent.futures import ThreadPoolExecutor


# Initialize once and share across modules
proj_config = ProjectConfig()
temp_proj_config = ProjectConfig()

# Singleton db object
DB_NAME = "SDV.db"

# EDA Output Data Formats
eda_output_data_formats = ["SYSTEMVERILOG HDL"]
fpga_boards = ["DE1-SoC Board",""]
fpga_devices = ["DE1-SoC Board",""]
simulation_tools = ["Questa Intel FPGA (SystemVerilog)"]
feedback_cycles = 5

# Global models
universal_big_model = "gpt-4o"
universal_small_model = "gpt-4o-mini"

# Thread pool
#executor = ThreadPoolExecutor(max_workers=6)


valid_llms=[
    "gpt-4o",           # GPT-4 Omni (April 2024), fast, multimodal, best overall
    "gpt-4o-mini",
    "gpt-4-turbo",      # GPT-4 Turbo (Nov 2023), cheaper/faster variant of GPT-4
    "gpt-4",            # Legacy GPT-4 (not always available)
    "gpt-3.5-turbo",    # Fast, cost-effective model
    "gpt-3.5",          # Legacy model name
    "text-davinci-003", # Legacy instruct model (from GPT-3 family)
    "text-davinci-002",
    "code-davinci-002", # Code generation model
    "gpt-4-0613",       # Dated GPT-4 version (June 2023 snapshot)
    "gpt-4-0314",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-0301"
]
        




