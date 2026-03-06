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

        with ui.card().classes('h-full flex-1 w-1/2 bg-white dark:!bg-[#1d2a3d]/80 rounded-2xl shadow-xl border border-slate-100 dark:border-slate-700 p-6'):
            with ui.row().classes('w-full justify-between items-center mb-4'):
                ui.label('HIL Dashboard').classes('text-2xl font-bold dark:text-gray-300 dark:text-slate-100 tracking-tight')

                self.bug_indicator = ui.label('⚠️ BUG INJECTION ACTIVE ⚠️') \
                    .classes('text-red-500 font-bold text-lg border-2 border-red-500 p-2 rounded animate-pulse hidden')

            # ---------------------------------------------------------
            # 1. Temperature Section
            # ---------------------------------------------------------
            ui.label('TEMPERATURE SENSOR').classes('text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-2')

            with ui.row().classes('w-full h-1/3 items-center justify-between gap-8'):

                self.temp_knob = CustomKnob(
                    value=25,
                    min=0,
                    max=100,
                    size=90,
                    color='red',
                    label='',
                    on_change=lambda val: self.callbacks['temp'](val)
                )

                with ui.row().classes('gap-3 bg-slate-50 dark:bg-slate-900/50 p-4 rounded-xl border border-slate-200 dark:border-slate-700 shadow-inner'):
                    self.temp_icon = ui.icon('circle', size='60px', color='slate-300').classes('transition-colors')

            ui.separator().classes('my-4 dark:bg-slate-700')

            # ---------------------------------------------------------
            # 2. Potentiometer Section
            # ---------------------------------------------------------
            ui.label('POTENTIOMETER (RPM)').classes('text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-2')

            with ui.row().classes('w-full h-1/3 items-center justify-between gap-8'):

                self.pot_knob = CustomKnob(
                    value=0,
                    min=0,
                    max=255,
                    size=90,
                    color='blue',
                    label='',
                    on_change=lambda val: self.callbacks['pot'](val)
                )


                with ui.row().classes('gap-3 bg-slate-50 dark:bg-slate-900/50 p-4 rounded-xl border border-slate-200 dark:border-slate-700 shadow-inner'):
                    for _ in range(4):
                        self.pot_leds.append(ui.icon('circle', size='60px', color='slate-300').classes('transition-colors'))

            ui.separator().classes('my-4 dark:bg-slate-700')

            # ---------------------------------------------------------
            # 3. Switch Section
            # ---------------------------------------------------------
            ui.label('MAIN SWITCH').classes('text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-2')

            with ui.row().classes('w-full h-1/3 items-center mt-2 justify-between'):
                self.switch = ui.switch(
                    on_change=lambda e: self.callbacks['switch'](e.value)
                ).classes('scale-200 origin-left transition-all duration-300').props('color=#08a4e5')
                with ui.row().classes('gap-3 bg-slate-50 dark:bg-slate-900/50 p-4 rounded-xl border border-slate-200 dark:border-slate-700 shadow-inner'):
                    self.switch_led = ui.icon('circle', size='60px', color='slate-300').classes('transition-colors')

    def update_view(self, feedback_colors: dict, bug: Optional[int]):


        # Temp update
        self.temp_icon.props(f'color={feedback_colors["temp"][0]}')
        self.temp_icon.style(f'text-shadow: {feedback_colors["temp"][1]}')

        # Pot LEDs update
        for i, led_icon in enumerate(self.pot_leds):
            led_icon.props(f'color={feedback_colors["pot_leds"][i][0]}')
            led_icon.style(f'text-shadow: {feedback_colors["pot_leds"][i][1]}')

        # Switch LED update
        self.switch_led.props(f'color={feedback_colors["switch"][0]}')
        self.switch_led.style(f'text-shadow: {feedback_colors["switch"][1]}')

        if bug is None:
            bug_active = False
        else:
            bug_active = True

        self.bug_indicator.set_visibility(bug_active)

        # if bug_active:
        #     self.bug_indicator.classes(add='animate-pulse')
        # else:
        #     self.bug_indicator.classes(remove='animate-pulse')