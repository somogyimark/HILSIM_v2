from src.model.dut import DUT


class MainController:
    def __init__(self, model: DUT):
        self.model = model
        self.view = None

    def register_view(self, view):
        self.view = view

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
        """A Dashboard 'BUG SIMULATION' gombja."""

        self.model.is_bug_active = not self.model.is_bug_active
        self.refresh_system()
    # --- Core Logic Update ---

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

        if self.view:

            self.view.update_view(model_data, colors, self.model.is_bug_active)