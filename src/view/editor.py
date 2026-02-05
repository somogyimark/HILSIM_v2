from nicegui import ui
import os


class EditorPanel:
    def __init__(self, callbacks):
        """
        callbacks: Dict {'run': func, 'save': func, 'load': func, 'logs': func}
        """
        self.callbacks = callbacks

        with ui.card().classes('w-full h-full column no-wrap'):
            ui.label('Test Automation & Fault Injection').classes('text-xl font-bold text-gray-200')

            default_code = (
                "batchControl -init\n"
                "batchControl -comment Start Test\n"
                "batchControl -start\n"
                "batchControl -hwfi temp 50\n"
                "batchControl -wait 1\n"
                "pause"
            )

            self.editor = ui.codemirror(value=default_code, language='Python', theme='vscodeDark') \
                .classes('w-full h-64 border border-gray-700 rounded')


            with ui.row().classes('w-full justify-between mt-2'):

                with ui.row():
                    ui.button('LOAD', on_click=self.callbacks['load'], color='blue')

                    ui.button('SAVE',
                              on_click=lambda: self.callbacks['save'](self.editor.value),
                              color='blue')

                    ui.button('LOGS', on_click=self.callbacks['logs'], color='grey')

                with ui.row():

                    ui.button('RUN SCRIPT', on_click=self.handle_run, color='green')

            ui.separator().classes('my-2')

            with ui.row().classes('w-full h-full column wrap'):
                ui.label('Console Output:').classes('text-sm font-bold text-gray-400')
                ui.button('Clear Log', on_click=lambda: self.log_output.clear(), color='grey').classes('mr-2')


            self.log_output = ui.log().classes('w-full h-48 bg-gray-900 text-green-400 p-2 rounded font-mono text-xs')

    async def handle_run(self):
        await self.callbacks['run'](self.editor.value)

    def append_log(self, message: str):
        self.log_output.push(message)

    def set_content(self, text: str):
        self.editor.value = text