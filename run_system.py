# run_system.py
import subprocess
import sys

def main():
    print("=== Step 1: Executing Olist Pipeline Training & Artifact Generation ===")
    pipeline_result = subprocess.run([sys.executable, "main.py"])
    
    if pipeline_result.returncode != 0:
        print("[Error] Pipeline execution failed.")
        sys.exit(1)
        
    print("\n=== Step 2: Launching FastAPI Real-Time Inference Server ===")
    subprocess.run(["uvicorn", "app:app", "--reload", "--port", "8000"])

if __name__ == "__main__":
    main()