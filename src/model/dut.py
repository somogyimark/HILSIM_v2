from typing import Dict, Optional
import random


class DUT:
    def __init__(self):
        self.hw_inputs: Dict[str, int] = {
            'pot': 0,
            'temp': 25,
            'switch': 0
        }
        self.swfi_inputs: Dict[str, Optional[int]] = {
            'pot': None,
            'temp': None,
            'switch': None
        }
        self.outputs: Dict[str, int] = {
            'pot_led': 1000,
            'temp_led': 0,
            'switch_led': 0,
        }

        self.bug: Optional[int] = None

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

    def set_bug_active(self, value: bool):
        if value:
            self.bug = random.randint(1, 4)
        else:
            self.bug = None

    def _update_temp_normal(self):
        self.outputs['temp_led'] = 1 if self.get_input('temp') > 30 else 0

    def _update_pot_normal(self):
        pot_val = self.get_input('pot')
        if pot_val < 64:
            self.outputs['pot_led'] = 1000
        elif pot_val < 128:
            self.outputs['pot_led'] = 1100
        elif pot_val < 192:
            self.outputs['pot_led'] = 1110
        else:
            self.outputs['pot_led'] = 1111

    def _update_switch_normal(self):
        self.outputs['switch_led'] = self.get_input('switch')

    def update_firmware(self):

        if self.bug is None:
            self._update_temp_normal()
            self._update_pot_normal()
            self._update_switch_normal()
            return

        match self.bug:
            case 1:
                self.outputs['switch_led'] = 0

                self._update_temp_normal()
                self._update_pot_normal()

            case 2:
                pot_val = self.get_input('pot')
                if pot_val < 74:
                    self.outputs['pot_led'] = 1000
                elif pot_val < 128:
                    self.outputs['pot_led'] = 1100
                elif pot_val < 192:
                    self.outputs['pot_led'] = 1110
                else:
                    self.outputs['pot_led'] = 1111

                self._update_temp_normal()
                self._update_switch_normal()

            case 3:
                pot_val = self.get_input('pot')
                if pot_val < 64:
                    self.outputs['pot_led'] = 1000
                elif pot_val < 128:
                    self.outputs['pot_led'] = 1100
                elif pot_val < 192:
                    self.outputs['pot_led'] = 1110
                else:
                    self.outputs['pot_led'] = 1110

                self._update_temp_normal()
                self._update_switch_normal()

            case 4:
                self.outputs['temp_led'] = 1 if self.get_input('temp') > 35 else 0

                self._update_pot_normal()
                self._update_switch_normal()