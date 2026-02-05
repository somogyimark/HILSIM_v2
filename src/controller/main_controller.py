import os
from datetime import datetime

import webview
from nicegui import ui, events, app
from src.model.hil_system import HILSystem
from src.model.script_executor import ScriptExecutor
from src.view.layout import MainLayout


class MainController:
    def __init__(self, hil_system: HILSystem):
        self.model = hil_system.dut
        self.hil = hil_system

        self.executor = ScriptExecutor(self.hil)

        self.view_dashboard = None
        self.view_editor = None

    def register_layout(self, layout: MainLayout):
        self.view_layout = layout
        self.view_dashboard = layout.dashboard
        self.view_editor = layout.editor
        self.refresh_system()

    # --- Event Handlers (User Inputs) ---

    def on_temp_change(self, value):
        self.model.set_hw_input('temp', value)
        self.refresh_system()

    def on_pot_change(self, value):
        self.model.set_hw_input('pot', value)
        self.refresh_system()

    def on_switch_change(self, value):
        self.model.set_hw_input('switch', value)
        self.refresh_system()

    def on_bug_toggle(self):

        self.model.is_bug_active = not self.model.is_bug_active
        self.refresh_system()

    async def on_run_script(self, code: str):
        if self.view_editor:
            await self.executor.run_script(code, self.view_editor.append_log)
            self.refresh_system()

    async def on_load_script(self):
        if not app.native.main_window:
            if self.view_editor:
                self.view_editor.append_log("Error: Not running in Native mode!")
            return

        initial_dir = os.path.abspath("scripts")

        dialog_type_open = 10

        try:
            file_selection = await app.native.main_window.create_file_dialog(
                dialog_type=dialog_type_open,
                directory=initial_dir,
                allow_multiple=False,
                file_types=('Batch files (*.bat)', 'All files (*.*)')
            )

            if file_selection and len(file_selection) > 0:
                file_path = file_selection[0]

                if isinstance(file_path, (list, tuple)):
                    file_path = file_path[0]

                if file_path.endswith(".bat"):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                        if self.view_editor:
                            self.view_editor.set_content(content)
                            ui.notify(f"Loaded: {os.path.basename(file_path)}", type='positive')

                    except Exception as e:
                        if self.view_editor:
                            ui.notify(f"Error reading file: {str(e)}", type='negative')
                else:
                    ui.notify(f"Error reading file: Wrong file type: [{file_path}]", type='negative')

        except Exception as e:
            print(f"Dialog Error: {e}")

    async def save_script_to_file(self, content: str):
        if not app.native.main_window:
            if self.view_editor:
                self.view_editor.append_log("Error: Not running in Native mode!")
            return

        initial_dir = os.path.abspath("scripts")

        dialog_type_open = 30

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scripts/test_script_{timestamp}.bat"

        try:
            file_selection = await app.native.main_window.create_file_dialog(
                dialog_type=dialog_type_open,
                directory=initial_dir,
                allow_multiple=False,
                save_filename= filename,
                file_types=('Batch files (*.bat)', 'All files (*.*)')
            )
            
            if not file_selection:
                return

            final_path = None

            if file_selection:
                if isinstance(file_selection, (list, tuple)):
                    if len(file_selection) > 0:
                        final_path = file_selection[0]
                elif isinstance(file_selection, str):
                    final_path = file_selection

            try:
                with open(final_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                if self.view_editor:
                    ui.notify(f"Saved: {final_path}", type='positive')

            except Exception as e:
                if self.view_editor:
                    ui.notify(f"Error reading file: {str(e)}", type='negative')
        except Exception as e:
            print(f"Dialog Error: {e}")

    def open_logs_folder(self):
        path = os.path.abspath("logs")
        os.startfile(path, 'open')

    def refresh_system(self):
        self.model.update_firmware()


        colors = {
            'temp': 'red' if self.model.outputs['temp_led'] else 'grey',
            'switch': 'green' if self.model.outputs['switch_led'] else 'grey',
            'pot_leds': []
        }

        potleds = [int(c) for c in str(self.model.outputs['pot_led'])]
        for led in potleds:
            colors['pot_leds'].append('green' if led == 1 else 'grey')


        if self.view_dashboard:
            self.view_dashboard.update_view(colors, self.model.is_bug_active)