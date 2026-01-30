import os
from datetime import datetime
from nicegui import ui
from src.model.hil_system import HILSystem
from src.model.script_executor import ScriptExecutor


class MainController:
    def __init__(self, hil_system: HILSystem):
        self.model = hil_system.dut
        self.hil = hil_system

        self.executor = ScriptExecutor(self.hil)

        self.view_dashboard = None
        self.view_editor = None

    def register_views(self, dashboard, editor):
        self.view_dashboard = dashboard
        self.view_editor = editor
        self.refresh_system()

    # --- Event Handlers (User Inputs) ---

    def on_temp_change(self, value):
        self.model.set_hw_input('temperature', value)
        self.refresh_system()

    def on_pot_change(self, value):
        self.model.set_hw_input('potmeter', value)
        self.refresh_system()

    def on_switch_change(self, value):

        val = 1 if value else 0
        self.model.set_hw_input('switch', val)
        self.refresh_system()

    def on_bug_toggle(self):

        self.model.is_bug_active = not self.model.is_bug_active
        self.refresh_system()

    async def on_run_script(self, code: str):
        if self.view_editor:
            await self.executor.run_script(code, self.view_editor.append_log)
            self.refresh_system()

    def on_load_script(self):
        pass

    def save_script_to_file(self, content: str):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scripts/test_script_{timestamp}.bat"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        if self.view_editor:
            self.view_editor.append_log(f"Script saved to: {filename}")
            ui.notify(f"Saved: {filename}", type='positive')

    def open_logs_folder(self):
        path = os.path.abspath("logs")
        os.startfile(path, 'open')

    def refresh_system(self):
        self.model.update_firmware()


        colors = {
            'temp': 'red' if self.model.outputs['temperature_led'] else 'grey',
            'switch': 'green' if self.model.outputs['switch_led'] else 'grey',
            'pot_leds': []
        }

        potleds = [int(c) for c in str(self.model.outputs['potmeter_led'])]
        for led in potleds:
            colors['pot_leds'].append('green' if led == 1 else 'grey')


        if self.view_dashboard:
            self.view_dashboard.update_view(colors, self.model.is_bug_active)