from typing import Dict, Any, Optional


class DUT:
    def __init__(self):
        self.hw_inputs: Dict[str, int] = {
            'potmeter': 0,
            'temperature': 25,
            'switch': 0
        }
        self.swfi_inputs: Dict[str, Optional[int]] = {
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

    def set_hw_input(self, component: str, value: int):
        self.hw_inputs[component] = value

    def clear_hw_input(self, component: str):
        if component in self.hw_inputs:
            del self.hw_inputs[component]

    def set_swfi_input(self, component: str, value: int):
        self.swfi_inputs[component] = value

    def clear_swfi_input(self, component: str):
        if component in self.swfi_inputs:
            del self.swfi_inputs[component]

    def get_input(self, component: str) -> int:
        if component in self.swfi_inputs and self.swfi_inputs[component] is not None:
            return self.swfi_inputs[component]
        return self.hw_inputs.get(component, 0)

    def update_firmware(self):
        """ temperature logic """
        if self.hw_inputs['temperature'] > 25:
            self.outputs['temperature_led'] = True
        else:
            self.outputs['temperature_led'] = False

        """ Potmeter logic """
        pot_val = self.get_input('potmeter')
        self.outputs['potmeter_led_1'] = True
        self.outputs['potmeter_led_2'] = pot_val > 25
        self.outputs['potmeter_led_3'] = pot_val > 50
        self.outputs['potmeter_led_4'] = pot_val > 75

        """ Switch Logic """
        switch_val = self.get_input('switch')

        if self.is_bug_active:

            self.outputs['switch_led'] = not bool(switch_val)
        else:
            self.outputs['switch_led'] = bool(switch_val)