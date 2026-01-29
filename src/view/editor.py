from nicegui import ui


class EditorPanel:
    def __init__(self, on_run_callback):
        self.on_run_callback = on_run_callback

        with ui.card().classes('w-full h-full column no-wrap'):
            ui.label('Test Automation & Fault Injection').classes('text-xl font-bold text-gray-200')


            default_code = (
                "# Példa Hiba Injektálásra (SWFI)\n"
                "# A Dashboardon a 'temp' 25 marad, de a rendszer 120-at lát!\n\n"
                "print('Starting Overheat Test...')\n"
                "dut.set_swfi_input('temperature', 120)\n"
                "print('Fault Injected: Temperature -> 120')\n"
            )

            self.editor = ui.codemirror(value=default_code, language='Python', theme='vscodeDark') \
                .classes('w-full h-64 border border-gray-700 rounded')

            with ui.row().classes('w-full justify-end mt-2'):
                ui.button('Clear Log', on_click=lambda: self.log_output.clear(), color='grey')
                ui.button('RUN SCRIPT', on_click=self.run_script, color='green')

            ui.separator().classes('my-2')

            ui.label('Console Output:').classes('text-sm font-bold text-gray-400')

            self.log_output = ui.log().classes('w-full h-48 bg-gray-900 text-green-400 p-2 rounded font-mono text-xs')

    def run_script(self):

        code = self.editor.value
        self.on_run_callback(code)

    def append_log(self, message: str):

        self.log_output.push(message)