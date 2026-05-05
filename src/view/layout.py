from nicegui import ui, app
from view.dashboard import DashboardPanel
from view.editor import EditorPanel


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

        ui.colors(primary='#08a4e5', secondary='#e2e8f0', accent='#08a4e5')

        self.build_ui()

    def build_ui(self):
        self.dark_mode_ctrl = ui.dark_mode(True)
        
        ui.query('body').classes('bg-[#f8fafc] dark:bg-[#0f172a] text-slate-800 dark:text-slate-200 font-sans antialiased overflow-hidden')

        with ui.header().classes('w-full flex justify-between items-center bg-white/80 dark:bg-[#1d2a3d]/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-700 shadow-sm p-0'):

            with ui.row().classes('grow h-full items-center gap-1 px-4 py-2 pywebview-drag-region'):
                ui.image('/assets/final_logo.png').classes('h-8 w-40 object-contain drop-shadow-sm')

            with ui.row().classes('items-center px-2 py-2'):
                ui.button(icon='settings', on_click=self.open_settings_dialog) \
                    .props('flat round dense') \
                    .classes('text-slate-500 hover:bg-slate-100 dark:hover:!bg-slate-700 hover:text-slate-800 transition-colors') \
                    .tooltip('Settings')

                ui.separator().props('vertical').classes('ml-2 mr-4 bg-slate-200 dark:bg-slate-700 h-8 w-0.5 rounded-full')

                ui.button(icon='remove',
                          on_click=lambda: app.native.main_window.minimize() if app.native else None) \
                    .props('flat round dense') \
                    .classes('text-slate-500 hover:bg-slate-100 dark:hover:!bg-slate-700 hover:text-slate-800 transition-colors')

                self.max_btn = ui.button(icon='crop_square', on_click=self.toggle_maximize) \
                    .props('flat round dense') \
                    .classes('text-slate-500 hover:bg-slate-100 dark:hover:!bg-slate-700 hover:text-slate-800 transition-colors')

                ui.button(icon='close', on_click=app.shutdown) \
                    .props('flat round dense') \
                    .classes('text-slate-500 hover:!bg-red-50 dark:hover:!bg-red-500 hover:!text-red-500 dark:hover:!text-red-300 transition-colors')

        with ui.row().classes('w-full h-[calc(100vh-82px)] no-wrap gap-6'):
            self.dashboard = DashboardPanel(self.dash_callbacks)
            self.editor = EditorPanel(self.editor_callbacks)
            
            def sync_dark_mode(e):
                val = e.value
                self.editor.editor.dark_mode = val
                self.dashboard.temp_knob.dark_mode = val
                self.dashboard.pot_knob.dark_mode = val

            sync_dark_mode(type('obj', (object,), {'value': self.dark_mode_ctrl.value}))
            self.dark_mode_ctrl.on_value_change(sync_dark_mode)

    def open_settings_dialog(self):
        with ui.dialog() as dialog, ui.card().classes('w-96 bg-white dark:!bg-slate-900 p-6 rounded-2xl shadow-2xl border border-slate-100 dark:border-slate-700'):
            ui.label('Settings').classes('text-xl font-bold mb-4 text-slate-800 dark:text-gray-300 tracking-tight')

            with ui.row().classes('w-full justify-between items-center mb-4'):
                ui.label('Dark Mode').classes('text-gray-700 dark:text-gray-300 font-medium')
                ui.switch().bind_value(self.dark_mode_ctrl)

            ui.label('Command Execution Delay').classes('text-gray-700 dark:text-gray-300 font-medium mb-2')

            with ui.column().classes('w-full gap-0'):

                ui.slider(min=0.0, max=2.0, step=0.1,
                          value=self.controller.executor.step_delay) \
                    .on('update:model-value', lambda e: self._update_delay(e.args)) \
                    .props('label-always')

            with ui.row().classes('w-full justify-between items-center mb-4'):
                ui.label('Bug Injection Active').classes('text-gray-700 dark:text-gray-300 font-medium text-red-600')

                current_state = self.controller.model.bug is not None
                ui.switch(value=current_state,
                          on_change=lambda e: self.controller.on_bug_toggle(e.value)) \
                    .props('color=red')

            with ui.row().classes('w-full justify-end mt-6'):
                ui.button('Close', on_click=dialog.close).classes('bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-600 shadow-sm rounded-lg px-4 py-2 font-medium transition-all')

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