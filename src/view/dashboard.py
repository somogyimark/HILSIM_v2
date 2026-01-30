from nicegui import ui


class DashboardPanel:
    def __init__(self, callbacks):
        """
        callbacks: {'temp': func, 'pot': func, 'switch': func, 'toggle_bug': func}
        """
        self.callbacks = callbacks
        self.pot_leds = []

        with ui.card().classes('w-full'):
            with ui.row().classes('w-full justify-between items-center mb-4'):
                ui.label('HIL Dashboard').classes('text-xl font-bold')
                self.btn_bug = ui.button('BUG SIMULATION', color='red',
                                         on_click=lambda: self.callbacks['toggle_bug']())

            # ---------------------------------------------------------
            # 1. Temperature Section
            # ---------------------------------------------------------
            ui.label('Temperature Sensor').classes('font-bold text-gray-400')

            with ui.row().classes('w-full items-center justify-start gap-8'):

                ui.knob(value=25, min=0, max=100, step=1, show_value=True,
                        color='red', track_color='grey-800', size='70px',
                        on_change=lambda e: self.callbacks['temp'](e.value))

                with ui.column().classes('items-center'):
                    self.temp_icon = ui.icon('thermostat', size='lg', color='grey')

            ui.separator().classes('my-4')

            # ---------------------------------------------------------
            # 2. Potentiometer Section
            # ---------------------------------------------------------
            ui.label('Potentiometer (RPM)').classes('font-bold text-gray-400')

            with ui.row().classes('w-full items-center justify-start gap-8'):

                ui.knob(value=0, min=0, max=255, step=1, show_value=True,
                        color='blue-500', track_color='blue-900', size='80px',
                        on_change=lambda e: self.callbacks['pot'](e.value))


                with ui.row().classes('gap-3 bg-gray-900 p-3 rounded-lg border border-gray-700'):
                    for _ in range(4):

                        self.pot_leds.append(ui.icon('circle', size='md', color='grey'))

            ui.separator().classes('my-4')

            # ---------------------------------------------------------
            # 3. Switch Section
            # ---------------------------------------------------------
            with ui.row().classes('w-full items-center mt-2 justify-between'):
                ui.label('Master Switch').classes('font-bold')
                with ui.row().classes('items-center'):
                    ui.switch(on_change=lambda e: self.callbacks['switch'](e.value))
                    self.switch_led = ui.icon('power_settings_new', size='md', color='grey').classes('ml-4')

    def update_view(self, feedback_colors: dict, bug_active: bool):
        # Temp update
        self.temp_icon.props(f'color={feedback_colors["temp"]}')

        # Pot LEDs update
        for i, led_icon in enumerate(self.pot_leds):
            led_icon.props(f'color={feedback_colors["pot_leds"][i]}')

        # Switch LED update
        self.switch_led.props(f'color={feedback_colors["switch"]}')


        if bug_active:
            self.btn_bug.props('outline')
        else:
            self.btn_bug.props(remove='outline')