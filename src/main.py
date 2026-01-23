from nicegui import ui
from model.dut import DUT


def main():
    dut = DUT()

    dut.set_hw_input('temp_sensor', 25.0)

    @ui.page('/')
    def index():
        ui.colors(led='red')
        ui.label('HIL Simulator Prototype').classes('text-2xl font-bold')

        with ui.card():
            ui.label('Temperature Sensor')

            result_label = ui.label()

            ui.slider(min=0, max=100, value=25.0,
                      on_change=lambda e: update_system(e.value))

            ui.icon('sym_r_thermostat', size='xl', color='led')
            def update_system(value):
                dut.set_hw_input('temp_sensor', value)
                effective_val = dut.get_input('temp_sensor')
                result_label.set_text(f'Effective Value: {effective_val:.1f} °C')
                ui.colors(led=f'{dut.update_physics(value)}')

            update_system(25.0)

    ui.run(title='HIL Sim', dark=True, native=True, window_size=(1200, 800))


if __name__ in {"__main__", "__mp_main__"}:
    main()