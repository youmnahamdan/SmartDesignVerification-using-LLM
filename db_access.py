import hashlib
import sqlite3
from threading import Lock

from DataClasses import *

class db_access:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        """Ensure the singleton pattern with thread safety."""
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        """Initialize the database connection and cursor."""
        if not hasattr(self, "_initialized"):  # To ensure __init__ only runs once
            import config 
            self.connection = sqlite3.connect(config.DB_NAME, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row  # Optional: makes query results dict-like
            self.cursor = self.connection.cursor()
            self._initialized = True

    def execute_query(self, query, parameters=None):
        """Execute a query (e.g., SELECT) and return the results."""
        if parameters is None:
            parameters = []
        try:
            self.cursor.execute(query, parameters)
            self.connection.commit()
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database query failed: {e}")
            return None

    def execute_command(self, command, parameters=None):
        """Execute a command (e.g., INSERT, UPDATE, DELETE)."""
        if parameters is None:
            parameters = []
        try:
            self.cursor.execute(command, parameters)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database command failed: {e}")
            return False
        
    def user_exists(self, user_email):
        """
        Check if a user exists in the database by their user_email.
        :param user_email: The user_email to check.
        :return: True if the user exists, False otherwise.
        """
        query = "SELECT 1 FROM users WHERE user_email = ? LIMIT 1"
        result = self.execute_query(query, (user_email,))
        return bool(result)
    
    def delete_user(self, user_id):
        """
        Delete a user from the database based on their user_id.
        :param user_id: The ID of the user to delete.
        :return: True if deleted successfully, False otherwise.
        """
        try:
            command = "DELETE FROM users WHERE user_id = ?"
            self.execute_command(command, (user_id,))
            return True
        except Exception as e:
            print(f"Failed to delete user: {e}")
            return False
        
    def check_password(self, email, password):
        query = "SELECT password FROM users WHERE user_email = ?"
        result = self.execute_query(query, (email,))
        if result:
            stored_password = result[0][0]  # (password,) tuple
            # how i hashed the password hashed_password = hashlib.sha256(password.encode()).hexdigest()
            hashed_input_password = hashlib.sha256(password.encode()).hexdigest()
            return stored_password == hashed_input_password
        return False
    
    def search_user(self, search_value):
        query = """
        SELECT user_id, user_name, user_email, access_level, password, rating
        FROM users
        WHERE user_id = ? OR user_email LIKE ? OR user_name LIKE ?
        """
        params = (search_value, f"%{search_value}%", f"%{search_value}%")
        return self.execute_query(query, params)

    def get_user(self, email):
        query = "SELECT * FROM users WHERE user_email = ?"
        result = self.execute_query(query, (email,))
        if result:
            row = list(result[0])
            user = User(
                user_id=row[0],
                user_name=row[1],
                user_email=row[2],
                access_level=row[3],
                password=row[4],
                rating=row[5]
                )
            return user
        return False
    
    def save_or_update_user(self, user_info):
        """
        Save a new user or update an existing user.
        :param user_info: tuple (user_id, username, email, access_level, password, rating)
        """
        try:
            user_id, username, email, access_level, password, rating = user_info
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Check if the user already exists
            query = "SELECT 1 FROM users WHERE user_id = ? LIMIT 1"
            result = self.execute_query(query, (user_id,))

            if result:
                # User exists -> Update
                command = """
                UPDATE users
                SET user_name = ?, user_email = ?, access_level = ?, password = ?, rating = ?
                WHERE user_id = ?
                """
                values = (username, email, access_level, hashed_password, rating, user_id)
            else:
                # User does not exist -> Insert
                command = """
                INSERT INTO users (user_id, user_name, user_email, access_level, password, rating)
                VALUES (?, ?, ?, ?, ?, ?)
                """
                values = (user_id, username, email, access_level, hashed_password, rating)

            return self.execute_command(command, values)

        except sqlite3.IntegrityError:
            print("User already exists or constraint error.")
            return False
        except Exception as e:
            print(f"Error saving or updating user: {e}")
            return False

    def close_connection(self):
        """Close the database connection."""
        self.connection.close()
        self._instance = None
        
    def insert_project(self, project: Project):
        query = """
            INSERT INTO projects (
                project_name, project_directory, no_api_calls, top_module_name, testbench_name,
                board, eda_output_format, simulation_tool, feedback_cycles, hdl, user_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(project_name) DO NOTHING;
        """
        params = (
            project.project_name,
            project.project_directory,
            project.no_api_calls,
            project.top_module_name,
            project.testbench_name,
            project.board,
            project.eda_output_format,
            project.simulation_tool,
            project.feedback_cycles,
            project.hdl,
            project.user_id
        )
        return self.execute_command(query, params)
    
    def update_api_calls(self, project_name, api_calls):
        query = " UPDATE projects SET no_api_calls = ? WHERE project_name = ?; "
        params = (api_calls, project_name)
        return self.execute_command(query, params)
    
    def get_project_by_name(self, project_name):
        query = "SELECT * FROM projects WHERE project_name = ?"
        results = self.execute_query(query, (project_name,))
        if results:
            row = list(results[0])
            project = Project(
                project_name=row[0],
                project_directory=row[1],
                no_api_calls=row[2],
                top_module_name=row[3],
                testbench_name=row[4],
                board=row[5],
                eda_output_format=row[6],
                simulation_tool=row[7],
                feedback_cycles=row[8],
                hdl=row[9],
                user_id=row[10]
            )
            return project
        return None
    
    def get_project_by_uid(self, user_id):
        query = "SELECT project_name, project_directory, no_api_calls, top_module_name, testbench_name, board, eda_output_format, simulation_tool, feedback_cycles, hdl  FROM projects WHERE user_id = ?"
        result = self.execute_query(query, (user_id,))
        return result
    
    def get_default_prompt_by_id(self, prompt_id):
        query = "SELECT d_prompt_id, d_prompt_name, d_prompt FROM default_prompts WHERE d_prompt_id = ?"
        result = self.execute_query(query, (prompt_id,))
        if result:
            result=list(result[0])
            return {
                "id": result[0],
                "name": result[1],
                "prompt": result[2]
            }
        
    def get_customized_prompts(self, user_id):
        query = "SELECT prompt_id, prompt_name, prompt FROM prompts WHERE user_id = ?;"
        result = self.execute_query(query, (user_id,))
        
        customized_prompts = {}
        for row in result:
            customized_prompts[row[1]] = row[2]
            
        if customized_prompts:
            return customized_prompts
        return False
    
    def save_customized_prompts(self, current_prompts, user_id):
        params = None
        query="""
INSERT INTO prompts (prompt_id, user_id, prompt_name, prompt)
VALUES (?, ?, ?, ?)
ON CONFLICT(user_id, prompt_id)
DO UPDATE SET
  prompt = excluded.prompt;
            """

        if current_prompts:
            for prompt_name, prompt in current_prompts.items():
                # insert/update
                if prompt_name == 'top_prompt':
                    params=(101, user_id, prompt_name, prompt,)
                    self.execute_command(query, params)
                elif prompt_name == 'driver_prompt':
                    params=(102, user_id, prompt_name, prompt,)
                    self.execute_command(query, params)
                elif prompt_name == 'design_prompt':
                    params=(103, user_id, prompt_name, prompt,)
                    self.execute_command(query, params)
                elif prompt_name == 'validation_prompt':
                    params=(104, user_id, prompt_name, prompt,)
                    self.execute_command(query, params)
                elif prompt_name == 'process_specs_prompt':
                    params=(105, user_id, prompt_name, prompt,)
                    self.execute_command(query, params)
                
    def delete_customized_prompts(self, user_id):
        # Define the query to delete the records
        query = """
        DELETE FROM prompts
        WHERE user_id = ?;
        """
        # Execute the query with the provided user_id as the parameter
        return self.execute_command(query, (user_id,))
    
    def delete_project(self, project_name):
        # Define the query to delete the records
        query = """DELETE FROM projects WHERE project_name = ?; """
        # Execute the query with the provided user_id as the parameter
        return self.execute_command(query, (project_name,))

    def get_project_directory(self, project_name):
        # Define the query to delete the records
        query = """SELECT project_directory FROM projects WHERE project_name = ?; """
        # Execute the query with the provided user_id as the parameter
        result = self.execute_query(query, (project_name,))
        if result:
            return result[0][0]

    
    
if __name__ == "__main__":
    db = db_access()
    '''project = Project( project_name="test_project",
                       project_directory="/path/to/project",
                       no_api_calls=0,
                       top_module_name="top_module",
                       testbench_name="testbench",
                       board="DE1-SoC Board",
                       eda_output_format="SYSTEMVERILOG HDL",
                       simulation_tool="Questa Intel FPGA (SystemVerilog)",
                       feedback_cycles=5,
                       hdl="verilog",
                       user_id=1)
    db.insert_project(project)

    for row in db.execute_query("Select * from projects;"):
        print(list(row))'''
        
    print('______________________________')
    print(db.get_default_prompt_by_id(101)['id'])
    print(db.get_default_prompt_by_id(101)['name'])
    print(db.get_default_prompt_by_id(101)['prompt'])
    print('______________________________')
    print(db.get_default_prompt_by_id(102)['id'])
    print(db.get_default_prompt_by_id(103)['name'])
    print(db.get_default_prompt_by_id(103)['prompt'])
    print('______________________________')
    print(db.get_default_prompt_by_id(104)['id'])
    print(db.get_default_prompt_by_id(104)['name'])
    print(db.get_default_prompt_by_id(104)['prompt'])
    print('______________________________')
    print(db.get_default_prompt_by_id(102)['id'])
    print(db.get_default_prompt_by_id(102)['name'])
    print(db.get_default_prompt_by_id(102)['prompt'])
    
        
