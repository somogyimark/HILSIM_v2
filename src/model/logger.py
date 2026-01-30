import os
from datetime import datetime
from src.utils import HTML_STYLE
import socket

def get_hostname() -> str:
    return socket.gethostname()

class HtmlLogger:
    def __init__(self):
        self.filepath = None

    def start_log(self, script_name: str):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"log_{timestamp}.html"
        self.filepath = os.path.join('logs', filename)

        with open(self.filepath, 'w', encoding='utf-8') as f:
            f.write(f"<html><head>{HTML_STYLE}</head><body>")
            f.write(f"<div class='div-base header'><h1>LOG CREATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h1>")
            f.write(f"<h3>HOST: {get_hostname()}</h3>")
            f.write(f"<h3>FROM: HILSIM</h3></div>")

    def log_comment(self, text: str):
        self._write("<div class='div-base task-log'>")
        self._write(f"<div class='comment'>{text}</div>")
        self._write("</div>")

    def log_generic(self, title: str, message: str):
        self._write("<div class='div-base task-log'>")
        self._write(f"<h2>{title}</h2><span>{message}</span>")
        self._write("</div>")

    def log_assert(self, item: dict):
        """
        Egyetlen assert eredményének logolása külön blokkba.
        item: {'param': 'temp', 'expected': 30, 'actual': 25, 'passed': False}
        """
        self._write("<div class='div-base task-log'>")
        res_class = "pass" if item['result'] == "PASS" else "fail"

        # Minden Assert külön 'div-base'-be kerül, hogy a CSS absolute pozicionálása
        # (left: 0, top: 0) ezen a dobozon belül legyen érvényes!
        html = f"""
            <div class='assert-header'>
                <h2>Assert</h2>
                <span>{datetime.now().strftime("%H:%M:%S")}</span>
            </div>

            <div class='assert-results'>
                <div class='assert-row-header'>
                    <div>Source</div>
                    <div>Measured</div>
                    <div>Assert Type</div>
                    <div>Expected</div>
                    <div>Result</div>
                </div>

                <div class='assert-row-data'>
                    <div>{item['source']}</div>
                    <div>{item['measured']}</div>
                    <div>{item['assertType']}</div>
                    <div>{item['expected']}</div>
                    <div class='{res_class}'>{item['result']}</div>
                </div>
            </div>
        """
        self._write(html)
        self._write("</div>")

    def close_log(self):
        if self.filepath:
            self._write("</body></html>")
            self.filepath = None

    def _write(self, content: str):
        if self.filepath:
            with open(self.filepath, 'a', encoding='utf-8') as f:
                f.write(content + "\n")