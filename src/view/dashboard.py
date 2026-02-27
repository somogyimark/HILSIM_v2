from typing import Optional

from nicegui import ui

from view.custom_knob import CustomKnob


class DashboardPanel:
    def __init__(self, callbacks):
        """
        callbacks: {'temp': func, 'pot': func, 'switch': func, 'toggle_bug': func}
        """
        self.callbacks = callbacks
        self.pot_leds = []

        with ui.card().classes('h-full w-full bg-white dark:!bg-[#1d2a3d]/80 rounded-2xl shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)] border border-slate-100 dark:border-slate-700 p-6'):
            with ui.row().classes('w-full justify-between items-center mb-4'):
                ui.label('HIL Dashboard').classes('text-2xl font-bold dark:text-gray-300 dark:text-slate-100 tracking-tight')

                self.bug_indicator = ui.label('⚠️ BUG INJECTION ACTIVE ⚠️') \
                    .classes('text-red-500 font-bold text-lg border-2 border-red-500 p-2 rounded animate-pulse hidden')

            # ---------------------------------------------------------
            # 1. Temperature Section
            # ---------------------------------------------------------
            ui.label('TEMPERATURE SENSOR').classes('text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-2')

            with ui.row().classes('w-full items-center justify-between gap-8'):

                self.temp_knob = CustomKnob(
                    value=25,
                    min=0,
                    max=100,
                    size=80,
                    color='#08a4e5',
                    label='',
                    on_change=lambda val: self.callbacks['temp'](val)
                )

                with ui.column().classes('items-center'):
                    self.temp_icon = ui.icon('thermostat', size='lg', color='slate-300')

            ui.separator().classes('my-4 dark:bg-slate-700')

            # ---------------------------------------------------------
            # 2. Potentiometer Section
            # ---------------------------------------------------------
            ui.label('POTENTIOMETER (RPM)').classes('text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-2')

            with ui.row().classes('w-full items-center justify-between gap-8'):

                self.pot_knob = ui.knob(value=0, min=0, max=255, step=1, show_value=True,
                        color='#08a4e5', track_color='#e2e8f0', size='80px', center_color='slate-700',
                        on_change=lambda e: self.callbacks['pot'](e.value))


                with ui.row().classes('gap-3 bg-slate-50 dark:bg-slate-900/50 p-4 rounded-xl border border-slate-200 dark:border-slate-700 shadow-inner'):
                    for _ in range(4):

                        self.pot_leds.append(ui.icon('circle', size='lg', color='slate-300'))

            ui.separator().classes('my-4 dark:bg-slate-700')

            # ---------------------------------------------------------
            # 3. Switch Section
            # ---------------------------------------------------------
            ui.label('MAIN SWITCH').classes('text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-2')

            with ui.row().classes('w-full items-center mt-2 justify-between'):
                self.switch = ui.switch(
                    on_change=lambda e: self.callbacks['switch'](e.value)
                ).classes('scale-150 origin-left transition-all duration-300').props('color=#08a4e5')
                self.switch_led = ui.icon('power_settings_new', size='lg', color='slate-300').classes('ml-4 transition-colors')

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