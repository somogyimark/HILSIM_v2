from turtle import color

from nicegui import ui
import os


class EditorPanel:
    def __init__(self, callbacks):
        """
        callbacks: Dict {'run': func, 'save': func, 'load': func, 'logs': func}
        """
        self.callbacks = callbacks
        self.current_file_path = None

        with ui.card().classes('w-full h-full column no-wrap'):
            self.current_file_name = ui.label().classes('text-xl font-bold text-gray-200 placeholder')

            default_code = (
                "batchControl -init\n"
                "batchControl -comment Start Test\n"
                "batchControl -start\n"
                "batchControl -hwfi temp 50\n"
                "batchControl -wait 1\n"
                "pause"
            )

            self.last_saved_content = default_code

            self.editor = ui.codemirror(value=default_code, language='Python', theme='vscodeDark') \
                .classes('w-full h-64 border border-gray-700 rounded')


            with ui.row().classes('w-full justify-between mt-2'):

                with ui.row():
                    ui.button('LOAD', on_click=self.callbacks['load'], color='blue')

                    ui.button('SAVE',
                              on_click=lambda: self.callbacks['save'](self.editor.value, self.current_file_path),
                              color='blue')

                    ui.button('LOGS', on_click=self.callbacks['logs'], color='grey')

                with ui.row():

                    ui.button('RUN SCRIPT', on_click=self.handle_run, color='green')

            ui.separator().classes('my-2')

            with ui.row().classes('w-full items-center gap-4'):
                ui.label('Console Output:').classes('text-sm font-bold text-gray-400')
                ui.button('Clear Log', on_click=lambda: self.log_output.clear(), color='grey').classes('mr-2')


            self.log_output = ui.log().classes('w-full h-48 bg-gray-900 text-green-400 p-2 rounded font-mono text-xs')

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
        with ui.dialog() as dialog, ui.card().classes('w-96 bg-gray-100 p-6'):
            ui.label('Do you want to save?').classes('text-xl font-bold mb-4 text-gray-800')

            with ui.row().classes('w-full h-full column wrap'):
                with ui.column():
                    ui.button('YES', on_click= lambda: dialog.submit(True), color='blue')
                with ui.column():
                    ui.button('NO',on_click= lambda: dialog.submit(False), color='red')

            with ui.row().classes('w-full justify-end mt-6'):
                ui.button('Close', on_click=dialog.close, color='primary')

        result = await dialog
        return result