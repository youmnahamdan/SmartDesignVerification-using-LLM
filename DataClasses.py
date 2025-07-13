from dataclasses import dataclass

@dataclass
class Project:
    project_name: str
    project_directory: str
    no_api_calls: int
    top_module_name: str
    testbench_name: str
    board: str
    eda_output_format: str
    simulation_tool: str
    feedback_cycles: int
    hdl: str
    user_id: int
    

@dataclass
class User:
    user_id: int
    user_name: str
    user_email: str
    access_level: int
    password: str
    rating: float
    








