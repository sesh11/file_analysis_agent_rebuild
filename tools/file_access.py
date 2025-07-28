from typing import Dict, Any
import pandas as pd
import subprocess
import os 

class FileAccessTool:
    def __init__(self):
        pass

    def get_definition(self) -> Dict[str, Any]:
        return{
            "function": {
                "name": "file_access",
                "description": ("Access a file and load it into a secure container for analysis")
            },
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Name of the file"
                    }
                },
                "required": ["filename"]
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        filename = arguments["filename"]
        return self.file_access(filename)
            
    def file_access(self, filename: str) -> str:
        print(f"🔍 FileAccessTool received filename: {filename}")
        print(f"🔍 File exists check: {os.path.isfile(filename)}")
        print(f"🔍 Path exists check: {os.path.exists(filename)}")
        print(f"🔍 Is absolute path: {os.path.isabs(filename)}")
    
        if not filename.endswith(".csv"):
                return("Not a valid file format")

        try:
            df = pd.read_csv(filename)
            output = self.copy_file_container(filename)
            return f"File copied successfully"

        except FileNotFoundError:
            return f"File not found"

        except Exception as e: 
            error_message = f"Error while reading the file: {str(e)}"
            return error_message

    def copy_file_container(self, filename: str, container_name: str = "sandbox") -> str:
        print(f"🔍 copy_file_container called with: {filename}")
        
        try:
            container_home_path = "/home/sandbox_user"
            if not os.path.isfile(filename):
                print(f"🔍 File check failed in copy_file_container")
                return f"❌ Source file not found: {filename}"

            print(f"🔍 Checking if container '{container_name}' is running...")
            
            # Check if container is running
            check_container = ["docker", "inspect", "-f", "{{.State.Running}}", container_name]
            response = subprocess.run(check_container, capture_output=True, text=True)
            print(f"🔍 Container check result: returncode={response.returncode}, stdout='{response.stdout.strip()}'")
            
            if response.returncode != 0 or response.stdout.strip() != "true":
                return f"❌ Container '{container_name}' is not running"

            print(f"🔍 Creating data directory in container...")
            
            # Create data directory in container
            mkdir_cmd = ["docker", "exec", container_name, "mkdir", "-p", "/home/sandbox_user/app/data"]
            mkdir_result = subprocess.run(mkdir_cmd, capture_output=True, text=True)
            print (f"mkdir result: {mkdir_result.returncode}, stderr: {mkdir_result.stderr}")


            #move the file to the container
            container_path = f"{container_name}:/home/sandbox_user/app/data/{os.path.basename(filename)}"
            copy_cmd = ["docker", "cp", filename, container_path]
            
            print(f"🔍 Running docker cp command: {' '.join(copy_cmd)}")
            copy_result = subprocess.run(copy_cmd, capture_output=True, text=True)
            
            print(f"🔍 Docker cp result:")
            print(f"    returncode: {copy_result.returncode}")
            print(f"    stdout: '{copy_result.stdout}'")
            print(f"    stderr: '{copy_result.stderr}'")

            if copy_result.returncode != 0:
                return f"❌ Docker copy failed: {copy_result.stderr}"
            
            print(f"🔍 Verifying file exists in container...")
            
            # Validate copy is complete
            verify_cmd = ["docker", "exec", container_name, "test", "-f", f"/home/sandbox_user/app/data/{os.path.basename(filename)}"]
            verify_result = subprocess.run(verify_cmd, capture_output=True, text=True)
            
            print(f"🔍 File verification result: returncode={verify_result.returncode}")
            
            if verify_result.returncode != 0:
                return f"FIle verification failed - find not found in container after copy"
            
            print(f"🔍 Copy completed successfully!")
            return f"✅ File '{os.path.basename(filename)}' copied successfully to container"
            
        except Exception as e:
            print(f"🔍 Exception in copy_file_container: {e}")
            return f"❌ Unexpected error during file copy: {str(e)}"
    
