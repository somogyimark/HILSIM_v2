from src.model.dut import DUT
from src.model.script_executor import ScriptExecutor


class MainController:
    def __init__(self, model: DUT):
        self.model = model
        self.executor = ScriptExecutor(model)

        self.view_dashboard = None
        self.view_editor = None

    def register_views(self, dashboard, editor):
        self.view_dashboard = dashboard
        self.view_editor = editor
        self.refresh_system()

    # --- Event Handlers (User Inputs) ---

    def on_temp_change(self, value):
        self.model.set_hw_input('temperature', value)
        self.refresh_system()

    def on_pot_change(self, value):
        self.model.set_hw_input('potmeter', value)
        self.refresh_system()

    def on_switch_change(self, value):

        val = 1.0 if value else 0.0
        self.model.set_hw_input('switch', val)
        self.refresh_system()

    def on_bug_toggle(self):

        self.model.is_bug_active = not self.model.is_bug_active
        self.refresh_system()

    def on_run_script(self, code: str):
        if self.view_editor:
            self.executor.execute(code, log_callback=self.view_editor.append_log)

        self.refresh_system()

    def refresh_system(self):
        self.model.update_firmware()


        colors = {
            'temp': 'red' if self.model.outputs['temperature_led'] else 'grey',
            'switch': 'green' if self.model.outputs['switch_led'] else 'grey',
            'pot_leds': []
        }

        for i in range(1, 5):
            is_on = self.model.outputs[f'potmeter_led_{i}']
            colors['pot_leds'].append('green' if is_on else 'grey')


        model_data = {
            'temp': self.model.get_input('temperature')
        }

        if self.view_dashboard:
            self.view_dashboard.update_view(model_data, colors, self.model.is_bug_active)