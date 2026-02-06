from nicegui import ui
from src.view.dashboard import DashboardPanel
from src.view.editor import EditorPanel


class MainLayout:
    def __init__(self, controller):

        self.dark_mode_ctrl = None
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
        self.dark_mode_ctrl = ui.dark_mode(True)

        with ui.header().classes('bg-blue-900 justify-between items-center text-white p-4'):
            with ui.row().classes('items-center gap-2'):
                ui.icon('memory', size='md')
                ui.label('HILSIM v2').classes('text-xl font-bold tracking-wider')

            ui.button(icon='settings', on_click=self.open_settings_dialog) \
                .props('flat round color=white') \
                .tooltip('Settings')

        with ui.row().classes('w-full h-screen no-wrap'):
            with ui.column().classes('w-1/2 p-4 bg-gray-900'):
                self.dashboard = DashboardPanel(self.dash_callbacks)

            with ui.column().classes('w-1/2 p-4 bg-gray-800'):
                self.editor = EditorPanel(self.editor_callbacks)

    def open_settings_dialog(self):
        with ui.dialog() as dialog, ui.card().classes('w-96 bg-gray-100 p-6'):
            ui.label('Settings').classes('text-xl font-bold mb-4 text-gray-800')

            with ui.row().classes('w-full justify-between items-center mb-4'):
                ui.label('Dark Mode').classes('text-gray-700 font-medium')
                ui.switch().bind_value(self.dark_mode_ctrl)

            ui.separator().classes('mb-4')

            ui.label('Script Execution Speed').classes('text-gray-700 font-medium mb-1')

            with ui.column().classes('w-full gap-0'):

                ui.slider(min=0.0, max=2.0, step=0.1,
                          value=self.controller.executor.step_delay) \
                    .on('update:model-value', lambda e: self._update_delay(e.args)) \
                    .props('label-always')

            with ui.row().classes('w-full justify-end mt-6'):
                ui.button('Close', on_click=dialog.close, color='primary')

        dialog.open()

    def _update_delay(self, value):
        self.controller.set_execution_delay(value)