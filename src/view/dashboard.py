from nicegui import ui, binding


class DashboardPanel:
    def __init__(self, on_temp_change_callback):
        self.on_temp_change = on_temp_change_callback

        with ui.card():
            ui.label('Temperature Sensor')

            self.result_label = ui.label('Effective Value: ---')

            ui.slider(min=0, max=100, value=25.0,
                      on_change=lambda e: self.on_temp_change(e.value))

            self.temp_icon = ui.icon('sym_r_thermostat', size='xl')

    def update_feedback(self, temp_value: float, color: str):
        self.result_label.set_text(f'Effective Value: {temp_value:.1f} °C')
        self.temp_icon.props(f'color={color}')