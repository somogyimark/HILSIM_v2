import os

HTML_STYLE = """
<style>
    body{ background-color: #002b3e; color: #edf2f4; font-family: Arial, sans-serif; width: 1350px; margin: auto; }
    .div-base{ margin: 10px; background-color: #005f8bb4; border-radius: 20px; padding: 20px; backdrop-filter: blur(8px); }
    .header{ margin-bottom: 40px; border-bottom: 1px solid #edf2f4; padding-bottom: 20px; }
    .task-log > h2{ margin-top: 10px; margin-bottom: 5px; }
    .task-log > span{ font-style: italic; font-size: 18px; display: inline-block; margin-bottom: 10px; }
    .comment{ padding: 20px; font-size: 18px; font-style: italic; color: #ffd166; }

    /* Assert Table Styles */
    .assert-container { display: flex; align-items: flex-start; margin-top: 10px; }
    .assert-header { 
        background-color: #003c57b2; padding: 15px; border-radius: 20px; 
        width: 120px; margin-right: 20px; text-align: center;
    }
    .assert-results { display: flex; flex-direction: column; }
    .assert-row { display: flex; margin-bottom: 2px; }
    .assert-cell {
        background-color: #003c57b2; padding: 10px; border-radius: 10px; 
        margin: 1px; width: 200px; text-align: center;
    }
    .assert-cell.header { background-color: #002b3fd7; font-weight: bold; }
    .pass { background-color: #38b000; font-weight: bold; }
    .fail { background-color: #ba181b; font-weight: bold; }
</style>
"""


def ensure_directories():

    os.makedirs('scripts', exist_ok=True)
    os.makedirs('logs', exist_ok=True)