from typing import Dict, Any, Optional


class DUT:
    def __init__(self):
        self.hw_inputs: Dict[str, float] = {}
        self.swfi_inputs: Dict[str, Optional[float]] = {}
        self.outputs: Dict[str, bool] = {}

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
        if component in self.swfi_inputs:
            return self.swfi_inputs[component]
        return self.hw_inputs.get(component, 0.0)