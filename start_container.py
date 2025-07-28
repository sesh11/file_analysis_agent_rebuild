#!/usr/bin/env python3
import subprocess
import os
import time

def start_container():
    """Start the Docker container for analysis"""
    
    # Change to sandbox directory
    sandbox_dir = os.path.join(os.path.dirname(__file__), "sandbox")
    os.chdir(sandbox_dir)
    
    print("🐳 Starting Docker container...")
    
    # Build and start container
    subprocess.run(["docker-compose", "up", "-d", "--build"], check=True)
    
    # Wait for container to be ready
    print("⏳ Waiting for container to be ready...")
    time.sleep(3)
    
    # Verify container is running
    result = subprocess.run(
        ["docker", "inspect", "-f", "{{.State.Running}}", "sandbox"],
        capture_output=True, text=True
    )
    
    if result.stdout.strip() == "true":
        print("✅ Container is running and ready for analysis!")
        return True
    else:
        print("❌ Container failed to start properly")
        return False

if __name__ == "__main__":
    start_container()