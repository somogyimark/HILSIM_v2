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
            'pot_led': 1000,
            'temp_led': 0,
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
        if self.swfi_inputs[component] is not None:
            return self.swfi_inputs[component]
        return self.hw_inputs[component]

    def get_output(self, component: str) -> int:
            return self.outputs[component]

    def update_firmware(self):
        """ temperature logic """
        if self.get_input('temperature') > 30:
            self.outputs['temp_led'] = 1
        else:
            self.outputs['temp_led'] = 0

        """ Potmeter logic """
        pot_val = self.get_input('potmeter')
        if pot_val < 64:
            self.outputs['pot_led'] = 1000
        elif pot_val < 128:
            self.outputs['pot_led'] = 1100
        elif pot_val < 192:
            self.outputs['pot_led'] = 1110
        else:
            self.outputs['pot_led'] = 1111

        """ Switch Logic """
        switch_val = self.get_input('switch')
        self.outputs['switch_led'] = switch_val
        # if self.is_bug_active:
        #
        #     self.outputs['switch_led'] = not bool(switch_val)
        # else:
        #     self.outputs['switch_led'] = bool(switch_val)