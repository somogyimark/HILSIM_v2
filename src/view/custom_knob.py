from nicegui.element import Element


class CustomKnob(Element, component='custom_knob.js'):
    def __init__(self, value: int, min: int, max: int, on_change, size, color,
                 label: str = None, dark_mode: bool = True):
        super().__init__()
        self._props['value'] = value
        self._props['min'] = min
        self._props['max'] = max
        self._props['size'] = size
        self._props['color'] = color
        self._props['dark_mode'] = dark_mode
        if label:
            self._props['label'] = label

        self.on('update:value', lambda e: self._handle_update(e.args, on_change))

    def _handle_update(self, new_value, on_change):
        self._props['value'] = new_value
        self.update()
        if on_change:
            on_change(new_value)

    @property
    def value(self):
        return self._props['value']

    @value.setter
    def value(self, new_value):
        self._props['value'] = new_value
        self.update()

    @property
    def dark_mode(self):
        return self._props.get('dark_mode', True)

    @dark_mode.setter
    def dark_mode(self, new_value: bool):
        self._props['dark_mode'] = new_value
        self.update()