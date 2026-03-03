from nicegui.element import Element

class CustomEditor(Element, component='custom_editor.js'):
    def __init__(self, value: str):
        super().__init__()
        self._props['value'] = value
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