from nicegui.element import Element


class CustomKnob(Element, component='custom_knob.js'):
    def __init__(self, value: int, min: int, max: int, on_change, size: int = 100, color: str = 'blue',
                 label: str = None):
        super().__init__()
        self._props['value'] = value
        self._props['min'] = min
        self._props['max'] = max
        self._props['size'] = size
        self._props['color'] = color
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