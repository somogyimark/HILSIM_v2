import os
import subprocess
import sys

# Need to find nicegui and rocher paths reliably
try:
    import nicegui
    import rocher
except ImportError:
    print("Dependencies not found! Please run pip install nicegui rocher")
    sys.exit(1)

nicegui_dir = os.path.dirname(nicegui.__file__)
rocher_dir = os.path.dirname(rocher.__file__)

pyinstaller_path = os.path.join('.venv', 'Scripts', 'pyinstaller.exe')

cmd = [
    pyinstaller_path,
    "--name", "HILSIM",
    "--onefile",
    "--windowed", # Hides the command prompt on launch
    "--add-data", f"{nicegui_dir};nicegui",
    "--add-data", f"{rocher_dir};rocher",
    "--add-data", f"assets;assets",
    "--add-data", f"src{os.sep}view{os.sep}*.js;view",
    "--paths", "src",
    "--icon", os.path.join("assets", "logo.ico"),
    "--collect-all", "Pillow",
    "--collect-all", "image_base64",
    "--collect-all", "rocher",
    os.path.join("src", "main.py")
]

print(f"Running command: {' '.join(cmd)}")
subprocess.run(cmd, check=True)
print("Build complete! Find the executable in the 'dist' folder.")
