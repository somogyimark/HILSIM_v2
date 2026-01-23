from typing import Dict, Any, Optional


class DUT:
    def __init__(self):
        self.hw_inputs: Dict[str, float] = {
            'potmeter': 0.0,
            'temperature': 25.0,
            'switch': 0
        }
        self.swfi_inputs: Dict[str, Optional[float]] = {
            'potmeter': None,
            'temperature': None,
            'switch': None
        }
        self.outputs: Dict[str, bool] = {
            'potmeter_led_1': True,
            'potmeter_led_2': False,
            'potmeter_led_3': False,
            'potmeter_led_4': False,
            'temperature_led': False,
            'switch_led': False,
        }

        self.is_bug_active: bool = False

    def set_hw_input(self, component: str, value: float):
        self.hw_inputs[component] = value

    def clear_hw_input(self, component: str):
        if component in self.hw_inputs:
            del self.hw_inputs[component]

    def set_swfi_input(self, component: str, value: float):
        self.swfi_inputs[component] = value

    def clear_swfi_input(self, component: str):
        if component in self.swfi_inputs:
            del self.swfi_inputs[component]

    def get_input(self, component: str) -> float:
        if component in self.swfi_inputs and self.swfi_inputs[component] is not None:
            return self.swfi_inputs[component]
        return self.hw_inputs.get(component, 0.0)

    def update_physics(self, value: float):

        self.hw_inputs['temperature'] = value

        if self.hw_inputs['temperature'] > 20.0:
            self.outputs['temperature_led'] = True
            return 'green'
        else:
            self.outputs['temperature_led'] = False
            return 'red'