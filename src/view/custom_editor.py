from nicegui.element import Element

class CustomEditor(Element, component='custom_editor.js'):
    def __init__(self, value: str, dark_mode: bool = False):
        super().__init__()
        self._props['value'] = value
        self._props['dark_mode'] = dark_mode
        self.on('update:value', self._handle_update)

    def _handle_update(self, e):
        self._props['value'] = e.args
            
    @property
    def value(self):
        return self._props['value']
        
    @value.setter
    def value(self, new_value):
        self._props['value'] = new_value
        self.update()

    @property
    def dark_mode(self):
        return self._props.get('dark_mode', False)

    @dark_mode.setter
    def dark_mode(self, new_value: bool):
        self._props['dark_mode'] = new_value
        self.update()