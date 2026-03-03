import os
from nicegui import ui, app
import rocher
from model.dut import DUT
from model.hil_system import HILSystem
from controller.main_controller import MainController
from view.layout import MainLayout
from utils import ensure_directories, resource_path, setup_taskbar_icon

def main():

    ensure_directories()
    setup_taskbar_icon()

    dut = DUT()
    hil_system = HILSystem(dut)
    controller = MainController(hil_system)

    assets_folder = resource_path('assets')
    icon_path = resource_path(os.path.join('assets', 'logo.ico'))
    app.add_static_files('/assets', assets_folder)
    app.add_static_files('/monaco-vs', rocher.path())

    @ui.page('/')
    def index():
        layout = MainLayout(controller)
        controller.register_layout(layout)

    app.native.window_args['frameless'] = True
    app.native.window_args['easy_drag'] = False

    ui.run(
        title='HIL SIM',
        dark=False,
        native=True,
        window_size=(1200, 800),
        reload=False,
        favicon=icon_path
    )


if __name__ in {"__main__", "__mp_main__"}:
    main()