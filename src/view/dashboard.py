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

        with ui.card().classes('h-full flex-1 w-1/2 bg-white dark:!bg-[#1d2a3d]/80 rounded-2xl shadow-xl border border-slate-100 dark:border-slate-700 p-6 relative overflow-hidden'):
            self.progress_bar = ui.linear_progress(show_value=False).props('indeterminate color="primary"').classes('absolute top-0 left-0 w-full z-50 hidden')

            # ---------------------------------------------------------
            # 1. Temperature Section
            # ---------------------------------------------------------
            with ui.row().classes('w-full justify-between items-right mb-4'):
                ui.label('TEMPERATURE SENSOR').classes('text-[2vh] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-2')
                self.bug_indicator = ui.label('⚠️ BUG INJECTION ACTIVE ⚠️') \
                        .classes('text-red-500 font-bold text-[2vh] border-2 border-red-500 rounded animate-pulse hidden')

            with ui.row().classes('w-full h-1/3 items-center justify-between gap-8'):

                self.temp_knob = CustomKnob(
                    value=25.00,
                    min=0.0,
                    max=100.0,
                    size='15vh',
                    color='red',
                    label='',
                    on_change=lambda val: self.callbacks['temp'](val),
                    step=0.01,
                    decimals=2
                )

                with ui.row().classes('gap-3 bg-slate-50 dark:bg-slate-900/50 p-4 rounded-xl border border-slate-200 dark:border-slate-700 shadow-inner'):
                    self.temp_icon = ui.icon('circle', size='7vh').classes('transition-colors text-slate-300 dark:text-[#717984]')

            ui.separator().classes('my-4 dark:bg-slate-700')

            # ---------------------------------------------------------
            # 2. Potentiometer Section
            # ---------------------------------------------------------
            ui.label('POTENTIOMETER').classes('text-[2vh] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-2')

            with ui.row().classes('w-full h-1/3 items-center justify-between gap-8'):

                self.pot_knob = CustomKnob(
                    value=0,
                    min=0,
                    max=255,
                    size='15vh',
                    color='blue',
                    label='',
                    on_change=lambda val: self.callbacks['pot'](val)
                )


                with ui.row().classes('gap-3 bg-slate-50 dark:bg-slate-900/50 p-4 rounded-xl border border-slate-200 dark:border-slate-700 shadow-inner'):
                    for _ in range(4):
                        self.pot_leds.append(ui.icon('circle', size='7vh').classes('transition-colors text-slate-300 dark:text-[#717984]'))

            ui.separator().classes('my-4 dark:bg-slate-700')

            # ---------------------------------------------------------
            # 3. Switch Section
            # ---------------------------------------------------------
            ui.label('MAIN SWITCH').classes('text-[2vh] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-2')

            with ui.row().classes('w-full h-1/3 items-center mt-2 justify-between'):
                self.switch = ui.switch(
                    on_change=lambda e: self.callbacks['switch'](e.value)
                ).classes('origin-left transition-all duration-300').props('color=#08a4e5 size=10vh')
                with ui.row().classes('gap-3 bg-slate-50 dark:bg-slate-900/50 p-4 rounded-xl border border-slate-200 dark:border-slate-700 shadow-inner'):
                    self.switch_led = ui.icon('circle', size='7vh').classes('transition-colors text-slate-300 dark:text-[#717984]')

    def update_view(self, feedback_colors: dict, bug: Optional[int]):

        def apply_color(icon, color_info):
            color, shadow = color_info
            if color == 'slate-300':
                icon.props(remove='color')
                icon.classes(add='text-slate-300 dark:text-[#717984]')
            else:
                icon.classes(remove='text-slate-300 dark:text-[#717984]')
                icon.props(f'color={color}')
            icon.style(f'text-shadow: {shadow}')

        # Temp update
        apply_color(self.temp_icon, feedback_colors["temp"])

        # Pot LEDs update
        for i, led_icon in enumerate(self.pot_leds):
            apply_color(led_icon, feedback_colors["pot_leds"][i])

        # Switch LED update
        apply_color(self.switch_led, feedback_colors["switch"])

        if bug is None:
            bug_active = False
        else:
            bug_active = True

        self.bug_indicator.set_visibility(bug_active)

        # if bug_active:
        #     self.bug_indicator.classes(add='animate-pulse')
        # else:
        #     self.bug_indicator.classes(remove='animate-pulse')

    def set_inputs_enabled(self, enabled: bool):
        if enabled:
            self.temp_knob.enable()
            self.pot_knob.enable()
            self.switch.enable()
            self.progress_bar.classes(remove='block', add='hidden')
        else:
            self.temp_knob.disable()
            self.pot_knob.disable()
            self.switch.disable()
            self.progress_bar.classes(remove='hidden', add='block')