from nicegui import ui, app
from model.dut import DUT
from pathlib import Path
from view.layout import build_interface
from controller.main_controller import MainController
from model.hil_system import HILSystem
from utils import ensure_directories


def main():
    ensure_directories()
    dut = DUT()
    hil_system = HILSystem(dut)
    controller = MainController(hil_system)

    BASE_DIR = Path(__file__).resolve().parent.parent
    app.add_static_files('/assets', BASE_DIR / 'assets')
    import base64

    def image_to_base64(path: str) -> str:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    LOGO_BASE64 = image_to_base64(r"D:\Szakdolgozat\HILSIM_v2\assets\logo.png")

    @ui.page('/')
    def index():
        dashboard, editor = build_interface(controller)

        controller.register_views(dashboard, editor)

    ui.run(title='HIL SIM', dark=True, native=True, window_size=(1200, 800), reload=False)


if __name__ in {"__main__", "__mp_main__"}:
    main()