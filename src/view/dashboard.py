from typing import Optional

from nicegui import ui

from src.view.custom_knob import CustomKnob


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

                self.bug_indicator = ui.label('⚠️ BUG INJECTION ACTIVE ⚠️') \
                    .classes('text-red-500 font-bold text-lg border-2 border-red-500 p-2 rounded animate-pulse hidden')

            # ---------------------------------------------------------
            # 1. Temperature Section
            # ---------------------------------------------------------
            ui.label('Temperature Sensor').classes('font-bold text-gray-400')

            with ui.row().classes('w-full items-center justify-between gap-8'):

                self.temp_knob = CustomKnob(
                    value=25,
                    min=0,
                    max=100,
                    size=80,
                    color='red',
                    label='',
                    on_change=lambda val: self.callbacks['temp'](val)
                )

                with ui.column().classes('items-center'):
                    self.temp_icon = ui.icon('thermostat', size='lg', color='grey')

            ui.separator().classes('my-4')

            # ---------------------------------------------------------
            # 2. Potentiometer Section
            # ---------------------------------------------------------
            ui.label('Potentiometer (RPM)').classes('font-bold text-gray-400')

            with ui.row().classes('w-full items-center justify-between gap-8'):

                self.pot_knob = ui.knob(value=0, min=0, max=255, step=1, show_value=True,
                        color='blue-500', track_color='blue-900', size='80px',
                        on_change=lambda e: self.callbacks['pot'](e.value))


                with ui.row().classes('gap-3 bg-gray-900 p-3 rounded-lg border border-gray-700'):
                    for _ in range(4):

                        self.pot_leds.append(ui.icon('circle', size='lg', color='grey'))

            ui.separator().classes('my-4')

            # ---------------------------------------------------------
            # 3. Switch Section
            # ---------------------------------------------------------
            ui.label('Switch').classes('font-bold')

            with ui.row().classes('w-full items-center mt-2 justify-between'):
                self.switch = ui.switch(
                    on_change=lambda e: self.callbacks['switch'](e.value)
                ).classes('scale-150 origin-left')
                self.switch_led = ui.icon('power_settings_new', size='lg', color='grey').classes('ml-4')

    def update_view(self, feedback_colors: dict, bug: Optional[int]):


        # Temp update
        self.temp_icon.props(f'color={feedback_colors["temp"]}')

        # Pot LEDs update
        for i, led_icon in enumerate(self.pot_leds):
            led_icon.props(f'color={feedback_colors["pot_leds"][i]}')

        # Switch LED update
        self.switch_led.props(f'color={feedback_colors["switch"]}')

        if bug is None:
            bug_active = False
        else:
            bug_active = True

        self.bug_indicator.set_visibility(bug_active)

        # if bug_active:
        #     self.bug_indicator.classes(add='animate-pulse')
        # else:
        #     self.bug_indicator.classes(remove='animate-pulse')