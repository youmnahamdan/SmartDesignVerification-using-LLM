import hashlib
from os import name
import sqlite3
from threading import Lock

from config import DB_NAME
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
            self.connection = sqlite3.connect(DB_NAME, check_same_thread=False)
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
                board, eda_output_format, simulation_tool, feedback_cycles, hdl, editors
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(project_name) DO UPDATE SET
                project_directory = excluded.project_directory,
                no_api_calls = excluded.no_api_calls,
                top_module_name = excluded.top_module_name,
                testbench_name = excluded.testbench_name,
                board = excluded.board,
                eda_output_format = excluded.eda_output_format,
                simulation_tool = excluded.simulation_tool,
                feedback_cycles = excluded.feedback_cycles,
                hdl = excluded.hdl,
                editors = excluded.editors
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
            project.editors
        )
        return self.execute_command(query, params)
    
    def get_project_by_name(self, project_name):
        query = "SELECT * FROM projects WHERE project_name = ?"
        results = self.execute_query(query, (project_name,))
        return results[0] if results else None






'''if __name__ == "__main__":
    db_obj = db_access()
    save_or_update_user
    new_proj = Project(
        project_name="my_project",
        project_directory="/path/to/project",
        no_api_calls=3,
        top_module_name="top_module",
        testbench_name="tb_top",
        row_id=101,
        board="DE10-Nano",
        eda_output_format="VCD",
        simulation_tool="ModelSim",
        feedback_cycles=2,
        hdl="Verilog",
        editors="VSCode"
    )
    
    success = db_obj.insert_project(new_proj)
    print(success)
    
    project = db_obj.get_project_by_name("my_project")
    if project:
        print(f"Project found: {project['project_name']}")
    else:
        print("Project not found.")
        
'''

db_obj = db_access()
db_obj.save_or_update_user((221133,'test', 'test', 4, 'test', 4.3))