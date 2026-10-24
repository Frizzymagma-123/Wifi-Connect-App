import sys
import subprocess
from flask import Flask

# 🧱 Direct Path Shielding to map modules out of system paths safely
sys.path.append(r"C:\Users\sanju\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\Local-packages\Python313\site-packages")

app = Flask(__name__)

@app.route('/scan', methods=['GET'])
def launch_my_python_app():
    """Triggers and executes your advanced multi-screen main.py application instantly."""
    try:
        # Path to your main.py file on your laptop desktop
        desktop_path = r"C:\Users\sanju\OneDrive\Attachments\Desktop\main.py"
        
        # This commands your computer terminal to run your exact purple app window code!
        subprocess.Popen(["python", desktop_path], creationflags=subprocess.CREATE_NO_WINDOW)
        return "Application Launched Successfully!"
    except Exception as e:
        return f"Launch Error: {str(e)}"

if __name__ == '__main__':
    # Starts the communication link gateway on your local home router
    app.run(host='0.0.0.0', port=5000)
