from typing import Dict, Any
import pandas as pd
import subprocess
import os 

class PythonExecTool:
    def __init__(self):
        pass

    def get_definition(self) -> Dict[str, Any]:
        return{
            "function": {
                "name": "execute_python",
                "description": ("Execute python code securely in a container. Python and the standard libraries needed to execute the analysis are already installed.")
            },
            "parameters": {
                "type": "object",
                "properties": {
                    "python_code": {
                        "type": "string",
                        "description": "Python code to be executed"
                    }
                },
                "required": ["python_code"]
            }
        }
    

    def execute(self, arguments: Dict[str, Any]) -> str:
        python_code = arguments["python_code"]
        python_code_stripped = python_code.strip('"""')
        output, errors = self._run_in_container(python_code_stripped)
        if errors:
            return f"Errors\n{errors}"
        
        return output
    
    @staticmethod
    def _run_in_container(code: str, container_name: str = "sandbox") -> tuple[str, str]:
        cmd = [
            "docker", "exec", "-i",
            container_name,
            "python", "-c", "import sys; exec(sys.stdin.read())"
        ]

        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out, err = process.communicate(code)
        return out, err
    