import os
from datetime import datetime
from src.utils import HTML_STYLE


class HtmlLogger:
    def __init__(self):
        self.filepath = None

    def start_log(self, script_name: str):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"log_{timestamp}.html"
        self.filepath = os.path.join('logs', filename)

        with open(self.filepath, 'w', encoding='utf-8') as f:
            f.write(f"<html><head>{HTML_STYLE}</head><body>")
            f.write(f"<div class='div-base header'><h1>Test Log: {script_name}</h1>")
            f.write(f"<h3>Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h3></div>")
            f.write("<div class='div-base task-log'>")

    def log_comment(self, text: str):
        self._write(f"<div class='comment'>Example Comment: {text}</div>")

    def log_generic(self, title: str, message: str):
        self._write(f"<h2>{title}</h2><span>{message}</span><hr>")

    def log_assert_group(self, asserts: list):

        html = "<div class='assert-container'>"

        html += """
        <div class='assert-header'>
            <h2>ASSERT</h2>
            <span>Check</span>
        </div>
        """

        html += "<div class='assert-results'>"

        html += """
        <div class='assert-row'>
            <div class='assert-cell header'>Parameter</div>
            <div class='assert-cell header'>Expected</div>
            <div class='assert-cell header'>Actual</div>
            <div class='assert-cell header'>Result</div>
        </div>
        """

        for item in asserts:
            res_class = "pass" if item['passed'] else "fail"
            res_text = "PASS" if item['passed'] else "FAIL"

            html += f"""
            <div class='assert-row'>
                <div class='assert-cell'>{item['param']}</div>
                <div class='assert-cell'>{item['expected']}</div>
                <div class='assert-cell'>{item['actual']}</div>
                <div class='assert-cell {res_class}'>{res_text}</div>
            </div>
            """

        html += "</div></div>"
        self._write(html)

    def close_log(self):
        if self.filepath:
            self._write("</div></body></html>")
            self.filepath = None

    def _write(self, content: str):
        if self.filepath:
            with open(self.filepath, 'a', encoding='utf-8') as f:
                f.write(content + "\n")