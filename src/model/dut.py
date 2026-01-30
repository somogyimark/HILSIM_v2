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
        self.outputs: Dict[str, int] = {
            'potmeter_led': 1000,
            'temperature_led': 0,
            'switch_led': 0,
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
        if self.hw_inputs['temperature'] > 30:
            self.outputs['temperature_led'] = 1
        else:
            self.outputs['temperature_led'] = 0

        """ Potmeter logic """
        pot_val = self.get_input('potmeter')
        if pot_val < 64:
            self.outputs['potmeter_led'] = 1000
        elif pot_val < 128:
            self.outputs['potmeter_led'] = 1100
        elif pot_val < 192:
            self.outputs['potmeter_led'] = 1110
        else:
            self.outputs['potmeter_led'] = 1111

        """ Switch Logic """
        switch_val = self.get_input('switch')
        self.outputs['switch_led'] = switch_val
        # if self.is_bug_active:
        #
        #     self.outputs['switch_led'] = not bool(switch_val)
        # else:
        #     self.outputs['switch_led'] = bool(switch_val)