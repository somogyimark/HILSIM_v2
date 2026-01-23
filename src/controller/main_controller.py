from src.model.dut import DUT


class MainController:
    def __init__(self, model: DUT):
        self.model = model
        self.view = None

    def register_view(self, view):
        self.view = view
        self.on_temp_change(25.0)

    def on_temp_change(self, value):
        self.model.set_hw_input('temperature', value)
        self.model.update_firmware()
        if self.model.outputs['temperature_led'] == True:
            color = 'green'
        else:
            color = 'red'

        self.view.update_feedback(self.model.hw_inputs['temperature'], color)