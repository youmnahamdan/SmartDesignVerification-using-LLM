'''
MODIFICATIONS TO DO:
EMULATION:
* SPECIFY THE COM AS VARIABLE
* RESEARCH JTAG @2 AND MODE
* MAKE EMULATION AT EVENT NOT AS PART OF THE SEQUECE
'''
import os
import subprocess
import asyncio
import re
import logging
import json
from config import proj_config, temp_proj_config
from time import time

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def create_script(proj_config, project_directory, script_name):
    if not os.path.exists(project_directory):
        os.makedirs(project_directory)
        
    script = os.path.join(project_directory,f"{script_name}.tcl")
    with open(script, 'w') as file:
        file.write(proj_config.get(script_name))
    
def save_code_files(project_directory, filename, code):
    """Saves the given SystemVerilog code string into a .sv file inside the project directory."""
    
    if not os.path.exists(project_directory):
        os.makedirs(project_directory)
    
    file_path = os.path.join(project_directory, filename)  # Ensure correct path
    pattern = r"```(?!\s*timescale)"
    code_cleaned = re.sub(pattern, '', code)
    code_cleaned = code_cleaned.replace("systemverilog", "")  
    try:
        with open(file_path, "w") as file:
            file.write(code_cleaned)
        logger.info(f"Code successfully saved to {file_path}")
    except Exception as e:
        logger.error(f"Error saving file: {e}")

async def extract_error_from_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            # Match errors like "Error (10112): some message ..."
            errors = re.findall(r'Error\s*\(\d+\):.*', content)
            return errors
    except Exception as e:
        return []

async def process_reports(files):
    tasks = [extract_error_from_file(file) for file in files]
    results = await asyncio.gather(*tasks)
    #no_errors = all(len(result) == 0 for result in results) 

    return results      

def set_pin_assignments(file_path): 
    try:
        result = subprocess.run(
            f"quartus_sh -t {file_path}", 
            shell=True, 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,  # Capture stderr as well
            text=True
        )
        # Combine stdout and stderr if you want both
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)
    
def quartus_synthesis_tool(design_name, code):
    temp_proj_config.set("PROJECT_NAME",design_name)
    temp_proj_config.set("TOP_LEVEL_ENTITY",design_name)
    temp_proj_config.set("PROJECT_DIRECTORY", f'{temp_proj_config.get("TEMP_DIRECTORY")}/{temp_proj_config.get("PROJECT_NAME")}')
    
    project_directory = temp_proj_config.get("PROJECT_DIRECTORY")
    create_script(temp_proj_config, project_directory, "quartus_script_temp_project_settings")
    create_script(temp_proj_config, project_directory, "quartus_script_temp_project_compilation")
   
    # Save code file
    file_name = f"{design_name}.sv"
    save_code_files(project_directory, file_name, code)
    
    try:
        # Step 1: Open or Create Project
        result = subprocess.run(
            f"quartus_sh -t quartus_script_temp_project_settings.tcl", 
            shell=True, 
            cwd=project_directory,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            logger.error(f"Error in opening project!: {result}")
            return
        
        # Step 2: Compile the Project
        logger.info("Synthesizing Code...")
        result = subprocess.run(
            f'start /B /wait cmd /c "quartus_sh -t quartus_script_temp_project_compilation.tcl"',
            shell=True,
            cwd=project_directory,
            capture_output=True,
            text=True
            )
        if result.returncode != 0:
            logger.error("Error in compilation! Logging...")
            return
        errors = asyncio.run(process_reports(temp_proj_config.get("REPORT_FILES")))
    
    except Exception as e:
        logger.error(e)
        
    # Create structured JSON
    structured_errors = {"errors": []}

    for group in errors:
        structured_errors["errors"].extend([err for err in group if err])
    
    return structured_errors

def complete_compilation_tool():
    project_directory = proj_config.get("PROJECT_DIRECTORY")
    create_script(proj_config, project_directory, "quartus_script_project_settings")
    create_script(proj_config, project_directory, "quartus_script_project_compilation")
    
    try:
        # Step 1: Open or Create Project
        result = subprocess.run(
            f"quartus_sh -t quartus_script_project_settings.tcl", 
            shell=True, 
            cwd=project_directory,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            logger.error(f"Error in opening project!: {result}")
            return
        
        # Step 2: Compile the Project
        logger.info("Compiling the Project...")
        result = subprocess.run(
            f'start  /B /wait  cmd /c "quartus_sh -t quartus_script_project_compilation.tcl"',
            shell=True,
            cwd=project_directory,
            text=True,
            stdout=subprocess.PIPE
            )
        if result.returncode != 0:
            logger.error("Error in compilation! Logging...")
            return
        
        return result.stdout
    except Exception as e:
        logger.error(e)
        
def ui_simulation_tool():
    directory = proj_config.get("PROJECT_DIRECTORY")

    logger.info("Running RTL Simulation...")
    result = subprocess.run(
        f'quartus_sh -t "{proj_config.get("NATIVELINK_DIRECTORY")}" --rtl_sim {proj_config.get("TOP_LEVEL_ENTITY")} {proj_config.get("TOP_LEVEL_ENTITY")}',
        shell=True,
        cwd=directory,
        text=True,
        stdout=subprocess.PIPE
    )
    if result.returncode != 0:
        logger.error(f"Error in simulation! {result.stderr}")
        return   
    return result.stdout
       
def questa_testbench_compilation_tool(code):
    # vlog -sv -work work +incdir+D:/NewQuartus/QuartusProjects/SelfTestingDesigns/AND D:/NewQuartus/QuartusProjects/SelfTestingDesigns/AND/tb1.sv
    project_directory = proj_config.get("PROJECT_DIRECTORY")
    tb_file_name = f'{proj_config.get("TEST_BENCH_NAME")}.sv'
    
    save_code_files(project_directory, tb_file_name, code)
    
    # Step 2: Compile the Project
    result = subprocess.run(
        f"vlog -sv -work work +incdir+{project_directory} {project_directory}/{tb_file_name}",
        shell=True,
        cwd=project_directory,
        text=True,
        stdout=subprocess.PIPE
    )

    # Combine stdout and stderr
    compilation_output = result.stdout
    
    return compilation_output

def create_testbench(internal_signals):
    monitor_string, monitor_signals, internal_signals_declaration, internal_signals_assignments = '', '', '', ''
    for signal, size in internal_signals.items():
        if len(size) > 0 and int(size) > 1 : 
            internal_signals_declaration += f"logic [{int(size)-1}:0] {signal};\n\t"     ##unsupported operand type(s) for -: 'str' and 'int'
        else:
            internal_signals_declaration += f"logic {signal};\n\t"
        internal_signals_assignments += f"assign {signal} = dut.{signal};\n\t"
        monitor_string += f'| {signal}=%h '
        monitor_signals += f', {signal}'
    
    tb_body = '''
`timescale 1ns / 1ps

module TEST_BENCH_NAME;

	logic clk;
	logic rst;
	logic [6:0] HEX_P0, HEX_P1, HEX_P2;
	logic [6:0] HEX_F0, HEX_F1, HEX_F2;


	INTERNAL_SIGNALS_DECLARATION
	

	// Instantiate the DUT (Device Under Test)
	TOP_LEVEL_ENTITY dut (
	  .clk(clk),
	  .rst(rst),
	  .HEX_P0(HEX_P0),
	  .HEX_P1(HEX_P1),
	  .HEX_P2(HEX_P2),
	  .HEX_F0(HEX_F0),
	  .HEX_F1(HEX_F1),
	  .HEX_F2(HEX_F2)
	);

	
	INTERNAL_SIGNALS_ASSIGNMENTS

	// Clock generation
	initial begin
	 clk = 0;
	 forever #10 clk = ~clk;
	end

	initial begin
	 $monitor($time, " clk=%b | rst=%b | HEX_P0=%b | HEX_P1=%b | HEX_P2=%b | HEX_F0=%b| HEX_F1=%b | HEX_F2=%b MONITOR_STRING ", clk, rst, HEX_P0, HEX_P1, HEX_P2, HEX_F0, HEX_F1, HEX_F2 MONITOR_SIGNALS);
	end

	initial begin
	 rst = 1; // Apply reset
	 #40;
	 rst = 0; // Release reset
	end

	initial begin
	 // Run simulation for a specific duration
	 #3000;
	 $stop; // Stop the simulation
	end

endmodule

'''
    tb_body = tb_body.replace("TEST_BENCH_NAME", proj_config.get("TEST_BENCH_NAME"))
    tb_body = tb_body.replace("TOP_LEVEL_ENTITY", proj_config.get("TOP_LEVEL_ENTITY"))
    tb_body = tb_body.replace("INTERNAL_SIGNALS_DECLARATION", internal_signals_declaration)
    tb_body = tb_body.replace("INTERNAL_SIGNALS_ASSIGNMENTS", internal_signals_assignments)
    tb_body = tb_body.replace("MONITOR_STRING", monitor_string)
    tb_body = tb_body.replace("MONITOR_SIGNALS", monitor_signals)
    
    save_code_files(proj_config.get("PROJECT_DIRECTORY"), proj_config.get("TEST_BENCH_NAME") + ".sv", tb_body)

def simulation_tool():
    directory = proj_config.get("PROJECT_DIRECTORY")

    logger.info("Running RTL Simulation...")
    result = subprocess.run(
        f'quartus_sh -t "{proj_config.get("NATIVELINK_DIRECTORY")}" --rtl_sim {proj_config.get("TOP_LEVEL_ENTITY")} {proj_config.get("TOP_LEVEL_ENTITY")}',
        shell=True,
        cwd=directory,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        logger.error(f"Error in simulation! {result.stderr}")
        return

def emulation_tool(cable, mode, device):
    project_directory = proj_config.get("PROJECT_DIRECTORY")
    sof_path = f'{proj_config.get("OUTPUT_FILES_DIRECTORY")}/{proj_config.get("TOP_LEVEL_ENTITY")}.sof'
    command = f'quartus_pgm -c {str(cable)} -m {mode} -o "p;{sof_path}@{device}"'
    try:
        # Run command
        process = subprocess.run(command, shell=True, cwd=project_directory, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        emulation_output = process.stdout.decode('utf-8', errors='ignore')
        return emulation_output
    except subprocess.CalledProcessError as e:
        stderr_output = e.stderr.decode('utf-8', errors='ignore')
        # Check for common port errors
        if "can't access JTAG chain" in stderr_output or "Error (213017): Cannot access JTAG" in stderr_output:
            return "JTAG port error: Check cable connection and permissions."
        elif "No such file or directory" in stderr_output:
            return f"File not found: {sof_path}"
        else:
            return f"Quartus programming failed:\n{stderr_output}\nCheck for improper connection and make sure the board is on."
    except Exception as e:
        return f"Unexpected error: {str(e)}"
    
def pin_assignments(file_path):
    subprocess.run(f"quartus_sh -t {file_path}",
        shell=True, 
        text=True           
    )
    
            


if __name__ == '__main__':
    st = time()
    settings = {
        "PROJECT_DIRECTORY": f'C:/Users/hp/OneDrive/Desktop/SDV/projects/self_testing_alu',
        "PROJECT_NAME": f'self_testing_alu',
        "TOP_LEVEL_ENTITY": f'self_testing_alu',
        "TEST_BENCH_NAME": f'tb_self_testing_alu',
    }    
                
    for key, value in settings.items():
        proj_config.set(key, value)
        

    dic = json.loads('{"pass_count":"[6:0]","fail_count":"[6:0]","stop":"[1:0]","test_input_a":"[3:0]","test_input_b":"[3:0]","actual_output":"[7:0]","expected_output":"[7:0]","control":"[2:0]"}')
    create_testbench(dic)
    print("Total compilation time is:  ", time()-st)


