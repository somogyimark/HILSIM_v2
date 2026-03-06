from turtle import color

from nicegui import ui
import os
from view.custom_editor import CustomEditor


class EditorPanel:
    def __init__(self, callbacks):
        """
        callbacks: Dict {'run': func, 'save': func, 'load': func, 'logs': func}
        """
        self.callbacks = callbacks
        self.current_file_path = None

        with ui.card().classes('flex-1 w-1/2 h-full column no-wrap bg-white dark:!bg-[#1d2a3d]/80 rounded-2xl shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)] border border-slate-100 dark:border-slate-700'):
            self.current_file_name = ui.label().classes('text-lg font-semibold text-slate-800 dark:text-slate-100 tracking-tight min-h-[18px] placeholder')

            default_code = (
                "batchControl -init\n"
                "batchControl -comment Start Test\n"
                "batchControl -start\n"
                "batchControl -hwfi temp 50\n"
                "batchControl -wait 1\n"
                "pause"
            )

            self.last_saved_content = default_code

            # self.editor = ui.codemirror(value=default_code, theme='github-light') \
            #     .classes('w-full h-64 border border-slate-200 dark:border-slate-700 rounded-xl overflow-hidden shadow-inner text-sm')

            self.editor = CustomEditor(value=default_code) \
                .classes('w-full h-48 border border-[#2a3441] rounded overflow-hidden')


            with ui.row().classes('w-full justify-between mt-4'):

                with ui.row().classes('gap-2'):
                    ui.button('LOAD', on_click=self.callbacks['load']) \
                        .props('outline color=primary') \
                        .classes('font-semibold rounded-lg hover:bg-slate-50 dark:hover:bg-slate-700 dark:text-slate-200 transition-colors')

                    ui.button('SAVE',
                              on_click=lambda: self.callbacks['save'](self.editor.value, self.current_file_path)) \
                        .props('outline color=primary') \
                        .classes('font-semibold rounded-lg hover:bg-slate-50 dark:hover:bg-slate-700 dark:text-slate-200 transition-colors')

                    ui.button('LOGS', on_click=self.callbacks['logs']) \
                        .props('flat text-color=grey-7') \
                        .classes('font-semibold rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 dark:text-slate-300 transition-colors')

                with ui.row():

                    ui.button('RUN SCRIPT', on_click=self.handle_run) \
                        .props('color=primary') \
                        .classes('font-bold rounded-lg px-6 shadow-md shadow-[#08a4e5]/20 hover:bg-[#0793ce] transition-colors')

            ui.separator().classes('my-4')

            with ui.row().classes('w-full items-center justify-between pb-2'):
                ui.label('CONSOLE OUTPUT').classes('text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider')
                ui.button('Clear Log', on_click=lambda: self.log_output.clear()) \
                    .props('flat outline text-color=grey-6 size=sm') \
                    .classes('font-medium hover:bg-slate-100 dark:hover:bg-slate-700 hover:text-slate-700 dark:hover:text-slate-200 rounded-lg transition-colors')



            self.log_output = ui.log().classes('w-full h-48 bg-gray-50 dark:bg-[#0f172a] text-[#38bdf8] p-4 rounded-xl shadow-inner font-mono text-xs overflow-hidden border border-slate-800 dark:border-slate-700')


    async def handle_run(self):
        await self.callbacks['run'](self.editor.value, self.current_file_path)

    def append_log(self, message: str):
        self.log_output.push(message)

    def set_content(self, text: str):
        self.editor.value = text

    def update_curr_filename(self, text: str):
        self.current_file_name.set_text(text)

    def get_curr_filename(self):
        return self.current_file.text

    def set_file_path(self, path):
        self.current_file_path = path

    def mark_as_saved(self, text: str):
        self.last_saved_content = text

    async def open_save_dialog(self) -> bool:
        with ui.dialog() as dialog, ui.card().classes('w-96 bg-white p-6 rounded-2xl shadow-2xl border border-slate-100'):
            ui.label('Do you want to save?').classes('text-xl font-bold mb-4 text-slate-800 tracking-tight')

            with ui.row().classes('w-full justify-end gap-3 mt-6'):
                ui.button('NO', on_click=lambda: dialog.submit(False)) \
                    .props('flat text-color=grey-7 outline') \
                    .classes('font-medium hover:bg-red-50 hover:text-red-600 rounded-lg')
                ui.button('YES', on_click=lambda: dialog.submit(True)) \
                    .props('color=primary') \
                    .classes('font-bold shadow-sm shadow-[#08a4e5]/20 rounded-lg')

            with ui.row().classes('hidden'):
                # We do not strictly need the extra Close button if they choose Yes/No, keeping original logic.
                ui.button('Close', on_click=dialog.close)

        result = await dialog
        return result