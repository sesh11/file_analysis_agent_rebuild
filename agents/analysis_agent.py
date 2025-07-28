import anthropic
from tools.file_access import FileAccessTool
from tools.execute_python import PythonExecTool
from util import util
import textwrap
import os

# filename = input('Enter the file that you wish to analyze')
# user_input = input('what is the analysis that you want to perform?')
# file_desc = input('provide additional information about the dataset')

class AnalysisAgent():
    def __init__(
            self,
            system_prompt: str = """
                You are an expert data analyst that is proficient in writing python code. You are extremely familiar with pandas and working with all types of datasets. 
                You will be provided with a file. Use the 'file_access' tool to copy the file from the directory to the docker sandbox environment. 
                The 'file_access' tool provides the information to orchestrate this. The file can found in the location /financials/data/ folder. Read the file and understand the data types, structures and columns. Columns are self-explanatory.
                After this use the 'execute_python' tool to execute the generated python against the file that is found in the folder /home/sandbox_user/app/data/" 
                Return the results of the execution of the python code back to the user. Ensure that all the execution of the python code is done in the sandbox environment.
            """
    ):
        self.setup_tools()
        self.system_prompt = system_prompt
        self.file_access = FileAccessTool()
        self.execute_python = PythonExecTool()

    
    def setup_tools(self) -> None:
        file_access = FileAccessTool()
        execute_python = PythonExecTool()


    def analyze(self, filename: str, user_input: str, file_desc: str, system_prompt: str = "") -> str:
        try:
            file_path = f"/Users/seshn/dev/claude/experiments/financials/data/{filename}"
            file_desc = file_desc or "No additional information provided"
            user_input = user_input or "No user input provided"

            copy_result = self.file_access.execute({"filename": file_path})
            if "successful" not in copy_result.lower():
                return f"Couldn't copy the file. {copy_result}"
            

            initial_prompt = f"""
            dataset: {filename}
            user request: {user_input}
            additional context: {file_desc}
            Generate ONLY python code to analyze the csv file. 
            Requirements: 
            - Return only executable python code, no explanations
            - Import the necessary libraries (pandas, etc.)
            - Load the CSV file from /home/sandbox_user/app/data/{filename}
            - Perform the analysis requested by the user
            - Print clear results
            - Handle exceptions gracefully

            IMPORTANT: Return only the Python code without any markdown explanations, formatting, or additional text.

            Example output format: 
            import pandas as pd
            import numpy as np
            df = pd.read_csv('/home/sandbox_user/app/data/data.csv)'
            """

            generated_code = util.invoke_claude(
                model="claude-3-5-sonnet-20240620",
                prompt=initial_prompt,
                system_prompt=self.system_prompt
            )    

            print("python code has been generated")
            print("executing code in the container ...........")

            result = self.execute_python.execute({"python_code": generated_code})
            
            if "error" in result:
                return f"Error in running the python code {result}"
            
            print("analysis is complete")
            return result
        
        except Exception as e:
            return f"analysis failed: {e}"

    
