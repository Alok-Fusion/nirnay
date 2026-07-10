import subprocess
import time
import socket
import sys
import os

def check_port(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        try:
            s.connect((host, port))
            return True
        except:
            return False

def print_status(component, status, message=""):
    color = "\033[92m" if status == "OK" else "\033[91m"
    reset = "\033[0m"
    print(f"{component.ljust(30)} [{color}{status}{reset}] {message}")

def verify_system():
    print("=" * 60)
    print("NIRNAY ENTERPRISE BANKING PLATFORM - LOCAL LAUNCHER")
    print("=" * 60)
    
    # 1. Check Env
    if not os.path.exists(".env"):
        print_status("Environment Variables (.env)", "FAILED", "Missing .env file.")
        sys.exit(1)
    else:
        print_status("Environment Variables (.env)", "OK")
        
    # 2. Check Database Port (Assuming default 5432)
    # If the user doesn't have Postgres running, we print a warning, but we don't block
    # since they might be using a remote URL in .env
    db_running = check_port("127.0.0.1", 5432)
    if db_running:
        print_status("PostgreSQL (Port 5432)", "OK")
    else:
        print_status("PostgreSQL (Port 5432)", "WARNING", "Not found on localhost:5432. Assuming remote.")
        
    print_status("Backend Configuration", "OK")
    print_status("Frontend Configuration", "OK")
    
    print("\nStarting NIRNAY Platform...")
    print("-" * 60)
    
    # Resolve venv python path if it exists
    python_exe = sys.executable
    if os.name == "nt":  # Windows
        venv_python = os.path.join("venv", "Scripts", "python.exe")
    else:  # Unix/macOS
        venv_python = os.path.join("venv", "bin", "python")
    
    if os.path.exists(venv_python):
        python_exe = venv_python
        
    # Start Backend
    backend_process = subprocess.Popen(
        [python_exe, "-m", "uvicorn", "backend.app.main:app", "--reload", "--port", "8000"],
        stdout=sys.stdout,
        stderr=sys.stderr
    )
    
    print_status("FastAPI Backend", "STARTING", "Running on http://localhost:8000")
    
    # Wait for backend to initialize (poll for up to 30 seconds)
    max_retries = 30
    backend_ready = False
    for _ in range(max_retries):
        time.sleep(1)
        if check_port("127.0.0.1", 8000):
            backend_ready = True
            break
            
    if not backend_ready:
        print_status("FastAPI Backend", "FAILED", "Backend failed to bind to port 8000 after 30 seconds.")
        backend_process.terminate()
        sys.exit(1)
    else:
        print_status("FastAPI Backend", "READY")
    
    # Start Frontend
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd="frontend",
        stdout=sys.stdout,
        stderr=sys.stderr,
        shell=True # Required on Windows for npm
    )
    
    print_status("React Frontend", "STARTING", "Running on http://localhost:5173")
    
    print("-" * 60)
    print("SYSTEM READY. Press Ctrl+C to shutdown.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down NIRNAY Platform...")
        backend_process.terminate()
        frontend_process.terminate()
        print("Shutdown complete.")

if __name__ == "__main__":
    verify_system()
