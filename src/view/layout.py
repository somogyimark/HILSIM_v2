from nicegui import ui
from src.view.dashboard import DashboardPanel
from src.view.editor import EditorPanel


def build_interface(controller):

    ui.colors(primary='#2b3d52', secondary='#384c63', accent='#ef4444')

    dash_callbacks = {
        'temp': controller.on_temp_change,
        'pot': controller.on_pot_change,
        'switch': controller.on_switch_change,
        'toggle_bug': controller.on_bug_toggle
    }
    editor_callbacks = {
        'run': controller.on_run_script,
        'save': controller.save_script_to_file,
        'load': controller.on_load_script,
        'logs': controller.open_logs_folder
    }


    with ui.row().classes('w-full h-screen no-wrap'):

        with ui.column().classes('w-1/2 p-4 bg-gray-900'):
            dashboard = DashboardPanel(dash_callbacks)

        with ui.column().classes('w-1/2 p-4 bg-gray-800'):
            editor = EditorPanel(editor_callbacks)

    return dashboard, editor