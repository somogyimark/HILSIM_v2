from nicegui import ui
from src.view.dashboard import DashboardPanel
from src.view.editor import EditorPanel


class MainLayout:
    def __init__(self, controller):

        self.controller = controller

        self.dash_callbacks = {
            'temp': controller.on_temp_change,
            'pot': controller.on_pot_change,
            'switch': controller.on_switch_change,
            'toggle_bug': controller.on_bug_toggle
        }

        self.editor_callbacks = {
            'run': controller.on_run_script,
            'save': controller.save_script_to_file,
            'load': controller.on_load_script,
            'logs': controller.open_logs_folder
        }

        ui.colors(primary='#2b3d52', secondary='#384c63', accent='#ef4444')

        self.build_ui()

    def build_ui(self):
        with ui.header().classes('bg-blue-900 justify-between items-center text-white'):
            ui.label('HILSIM').classes('text-lg font-bold')
            ui.switch('Dark Mode', value=True,
                      on_change=lambda e: ui.dark_mode(e.value))

        with ui.row().classes('w-full h-screen no-wrap'):
            with ui.column().classes('w-1/2 p-4 bg-gray-900'):
                self.dashboard = DashboardPanel(self.dash_callbacks)

            with ui.column().classes('w-1/2 p-4 bg-gray-800'):
                self.editor = EditorPanel(self.editor_callbacks)