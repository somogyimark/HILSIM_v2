from nicegui import ui, app
from model.dut import DUT
from pathlib import Path
from view.layout import build_interface
from controller.main_controller import MainController


def main():
    dut = DUT()
    controller = MainController(dut)

    BASE_DIR = Path(__file__).resolve().parent.parent
    app.add_static_files('/assets', BASE_DIR / 'assets')

    @ui.page('/')
    def index():
        dashboard, editor = build_interface(controller)

        controller.register_views(dashboard, editor)

    ui.run(title='HIL SIM', dark=True, native=True, window_size=(1200, 800), reload=False)


if __name__ in {"__main__", "__mp_main__"}:
    main()