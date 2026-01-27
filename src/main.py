from nicegui import ui, app
from model.dut import DUT
from pathlib import Path
from view.dashboard import DashboardPanel
from controller.main_controller import MainController


def main():
    dut = DUT()
    controller = MainController(dut)


    callbacks = {
        'temp': controller.on_temp_change,
        'pot': controller.on_pot_change,
        'switch': controller.on_switch_change,
        'toggle_bug': controller.on_bug_toggle
    }

    @ui.page('/')
    def index():
        ui.label('HIL Simulator Prototype').classes('text-2xl font-bold')
        BASE_DIR = Path(__file__).resolve().parent.parent
        app.add_static_files('/assets', BASE_DIR / 'assets')

        dashboard = DashboardPanel(callbacks)
        controller.register_view(dashboard)

    ui.run(title='HIL SIM', dark=True, native=True, window_size=(1200, 800), reload=False)


if __name__ in {"__main__", "__mp_main__"}:
    main()