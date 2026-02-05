import os
import sys
import ctypes
from src.image_base64 import image_to_base64

def ensure_directories():

    os.makedirs('scripts', exist_ok=True)
    os.makedirs('logs', exist_ok=True)

def setup_taskbar_icon():
    if sys.platform.startswith('win'):
        try:
            myappid = 'mycompany.hilsim.simulator.v1'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception as e:
            print(f"Could not set AppUserModelID: {e}")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

assets_folder = resource_path('assets')
LOGO_PATH = resource_path(os.path.join('assets', 'logo.png'))
LOGO_BASE64 = image_to_base64(LOGO_PATH)

HTML_STYLE = f"""
<style>
    body {{
        background-color: #002b3e;
        /* background: radial-gradient(#00608b, #002b3e); */
        color: #edf2f4;
        
        background-image: url("data:image/png;base64,{LOGO_BASE64}");
        background-position: center center;
        background-repeat: no-repeat;
        background-size: 40%;
        background-attachment: fixed;

        width: 1350px;
        margin: auto;
    }}
    .div-base{{
    margin: 10px;
    background-color: #005f8bb4;
    border-radius: 20px;
    padding-left: 20px;
    padding-right: 20px;
    padding-top: 5px;
    padding-bottom: 5px;
    backdrop-filter: blur(8px);
    position: relative;
    }}
    .header{{
    margin-bottom: 40px;
    font-family: Arial, Helvetica, sans-serif;
    padding-bottom: 20px;
    }}
    
    .header > h1{{
        margin-bottom: 10px;
    }}
    
    .header > h3{{
        margin-top: 5px;
        margin-bottom: 5px;
    }}
    
    .task-log > h2{{
        margin-top: 10px;
        margin-bottom: 5px;
        font-family: Arial, Helvetica, sans-serif;
    }}
    
    .task-log > span{{
        font-style: italic;
        font-size: 18px;
        display: inline-block;
        margin-bottom: 10px;
    }}
    
    .comment{{
        padding-top: 15px;
        padding-bottom: 15px;
        font-size: 18px;
        font-style: italic;
    }}
    
    .assert-header{{
        display: inline-block;
        background-color: #003c57b2;
        padding-left: 15px;
        padding-right: 20px;
        border-radius: 20px;
        position: absolute;
        top: 0px;
        left: 0px;
        margin-top: 5px;
        margin-left: 5px;
        margin-bottom: 5px;
        height: calc(100% - 10px);
        width: 120px;
    }}
    
    .assert-header > h2{{
        margin-top: 10px;
        margin-bottom: 5px;
        font-family: Arial, Helvetica, sans-serif;
    }}
    
    .assert-header > span{{
        font-style: italic;
        font-size: 18px;
        display: inline-block;
        margin-bottom: 10px;
    }}
    
    .assert-results{{
        display: inline-block;
        margin-left: 162px;
    }}
    
    .assert-row-header{{
        display: inline-block;
    }}
    
    .assert-row-header > div{{
        display: inline-block;
        background-color: #002b3fd7;
        padding: 10px;
        border-radius: 10px;
        margin-left: -1px;
        margin-right: -1px;
        width: 200px;
        text-align: center;
    }}
    
    .assert-row-data > div{{
        display: inline-block;
        background-color: #003c57b2;
        padding: 10px;
        border-radius: 10px;
        margin-left: -1px;
        margin-right: -1px;
        margin-top: 2px;
        width: 200px;
        text-align: center;
    }}
    
    .assert-row-data > .pass{{
        background-color: #38b000;
        font-family: Arial, Helvetica, sans-serif;
        font-weight: bold;
    }}
    
    .assert-row-data > .fail{{
        background-color: #ba181b;
        font-family: Arial, Helvetica, sans-serif;
        font-weight: bold;
    }}
</style>
"""