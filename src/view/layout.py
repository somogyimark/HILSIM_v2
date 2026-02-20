from nicegui import ui, app
from src.view.dashboard import DashboardPanel
from src.view.editor import EditorPanel


class MainLayout:
    def __init__(self, controller):

        self.dark_mode_ctrl = None
        self.controller = controller
        self.is_maximized = False

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

        with ui.header().classes('w-full flex justify-between items-center bg-[#0b1426] border-b border-[#2a3441] p-0'):

            with ui.row().classes('grow h-full items-center gap-3 px-4 py-2 pywebview-drag-region'):
                ui.image('/assets/final_logo.png').classes('h-8 w-40 object-contain')

            with ui.row().classes('items-center gap-1 px-4 py-2'):
                ui.button(icon='settings', on_click=self.open_settings_dialog) \
                    .props('flat round dense color=grey') \
                    .tooltip('Settings')

                ui.separator().props('vertical').classes('mx-2 bg-[#2a3441] h-6')

                ui.button(icon='remove',
                          on_click=lambda: app.native.main_window.minimize() if app.native else None) \
                    .props('flat round dense color=grey') \
                    .classes('hover:bg-gray-800 transition-colors')

                self.max_btn = ui.button(icon='crop_square', on_click=self.toggle_maximize) \
                    .props('flat round dense color=grey') \
                    .classes('hover:bg-gray-800 transition-colors')

                ui.button(icon='close', on_click=app.shutdown) \
                    .props('flat round dense color=grey') \
                    .classes('hover:bg-red-600 hover:text-white transition-colors')

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

            ui.label('Command Execution Delay').classes('text-gray-700 font-medium mb-2')

            with ui.column().classes('w-full gap-0'):

                ui.slider(min=0.0, max=2.0, step=0.1,
                          value=self.controller.executor.step_delay) \
                    .on('update:model-value', lambda e: self._update_delay(e.args)) \
                    .props('label-always')

            with ui.row().classes('w-full justify-between items-center mb-4'):
                ui.label('Bug Injection Active').classes('text-gray-700 font-medium text-red-600')

                current_state = self.controller.model.bug is not None
                ui.switch(value=current_state,
                          on_change=lambda e: self.controller.on_bug_toggle(e.value)) \
                    .props('color=red')

            with ui.row().classes('w-full justify-end mt-6'):
                ui.button('Close', on_click=dialog.close, color='primary')

        dialog.open()

    def _update_delay(self, value):
        self.controller.set_execution_delay(value)

    def toggle_maximize(self):
        if not app.native:
            return

        if self.is_maximized:
            app.native.main_window.restore()
            self.max_btn.props('icon=crop_square')
        else:
            app.native.main_window.maximize()
            self.max_btn.props('icon=filter_none')

        self.is_maximized = not self.is_maximized