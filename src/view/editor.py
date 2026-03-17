from turtle import color

from nicegui import ui
import os
from view.custom_editor import CustomEditor


class EditorPanel:
    def __init__(self, callbacks):
        """
        callbacks: Dict {'run': func, 'save': func, 'load': func, 'logs': func}
        """
        self.callbacks = callbacks
        self.pages = []
        self.active_page_id = None
        self.page_counter = 0

        with ui.card().classes('flex-1 w-1/2 h-full column no-wrap bg-white dark:!bg-[#1d2a3d]/80 rounded-2xl shadow-xl border border-slate-100 dark:border-slate-700'):
            
            with ui.row().classes('w-full relative group items-end flex-nowrap min-h-[40px] border-b border-slate-200 dark:border-slate-700'):
                self.tabs_container = ui.row().classes('flex-1 overflow-x-auto gap-1 no-wrap items-end h-[40px] px-2 pt-2 scrollbar-hidden')
                ui.button(icon='add', on_click=lambda: self.add_new_page()) \
                    .props('flat round size=sm') \
                    .classes('opacity-0 group-hover:opacity-100 transition-opacity mx-2 shrink-0 self-center text-slate-500 hover:text-blue-500')

            self.editor = CustomEditor(value="") \
                .classes('w-full h-48 border-b border-slate-200 dark:border-slate-700 overflow-hidden')
            
            self.editor.on('update:value', self.on_editor_update)

            default_code = (
                "batchControl -init\n"
                "batchControl -comment Start Test\n"
                "batchControl -start\n"
                "batchControl -hwfi temp 50\n"
                "batchControl -wait 1\n"
                "pause"
            )

            self.add_new_page(content=default_code)


            with ui.row().classes('w-full justify-between mt-4'):

                with ui.row().classes('gap-2'):
                    ui.button('LOAD', on_click=self.callbacks['load']) \
                        .props('outline color=primary size=2vh') \
                        .classes('font-semibold rounded-lg hover:bg-slate-50 dark:hover:bg-slate-700 dark:text-slate-200 transition-colors')

                    ui.button('SAVE',
                              on_click=lambda: self.callbacks['save'](self.editor.value, self.current_file_path)) \
                        .props('outline color=primary size=2vh') \
                        .classes('font-semibold rounded-lg hover:bg-slate-50 dark:hover:bg-slate-700 dark:text-slate-200 transition-colors')

                    ui.button('LOGS', on_click=self.callbacks['logs']) \
                        .props('flat text-color=grey-7 size=2vh') \
                        .classes('font-semibold rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 dark:text-slate-300 transition-colors')

                with ui.row():

                    ui.button('RUN SCRIPT', on_click=self.handle_run) \
                        .props('color=primary size=2vh') \
                        .classes('font-bold rounded-lg px-6 shadow-md shadow-[#08a4e5]/20 hover:bg-[#0793ce] transition-colors')

            ui.separator().classes('my-4')

            with ui.row().classes('w-full items-center justify-between pb-2'):
                ui.label('CONSOLE OUTPUT').classes('text-[1.5vh] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider')
                ui.button('Clear Log', on_click=lambda: self.log_output.clear()) \
                    .props('flat outline text-color=grey-6 size=sm size-1.5vh') \
                    .classes('font-medium hover:bg-slate-100 dark:hover:bg-slate-700 hover:text-slate-700 dark:hover:text-slate-200 rounded-lg transition-colors')



            self.log_output = ui.log().classes('w-full h-48 bg-gray-50 dark:bg-[#0f172a] text-[#38bdf8] p-4 rounded-xl shadow-inner font-mono text-xs overflow-hidden border border-slate-200 dark:border-slate-700')


    async def handle_run(self):
        await self.callbacks['run'](self.editor.value, self.current_file_path)

    def append_log(self, message: str):
        self.log_output.push(message)

    @property
    def current_file_path(self):
        p = self.get_active_page()
        return p['path'] if p else None

    @current_file_path.setter
    def current_file_path(self, path):
        p = self.get_active_page()
        if p:
            p['path'] = path

    @property
    def last_saved_content(self):
        p = self.get_active_page()
        return p['saved_content'] if p else ""

    def add_new_page(self, name=None, content=""):
        if not name:
            self.page_counter += 1
            name = f"Untitled-{self.page_counter}"

        page_id = self.page_counter
        self.page_counter += 1

        new_page = {
            'id': page_id,
            'name': name,
            'content': content,
            'path': None,
            'saved_content': content
        }
        self.pages.append(new_page)
        self.switch_to_page(page_id)

    def close_page(self, page_id):
        idx = next((i for i, p in enumerate(self.pages) if p['id'] == page_id), -1)
        if idx == -1: return

        self.pages.pop(idx)

        if len(self.pages) == 0:
            self.add_new_page()
        elif self.active_page_id == page_id:
            new_idx = max(0, idx - 1)
            self.switch_to_page(self.pages[new_idx]['id'])
        else:
            self.render_tabs()

    def switch_to_page(self, page_id):
        if self.active_page_id is not None:
            active_page = self.get_active_page()
            if active_page:
                active_page['content'] = self.editor.value

        self.active_page_id = page_id
        new_active = self.get_active_page()
        if new_active:
            self.editor.value = new_active['content']
            
        self.render_tabs()

    def get_active_page(self):
        for p in self.pages:
            if p['id'] == self.active_page_id:
                return p
        return None

    def on_editor_update(self, e):
        page = self.get_active_page()
        if page:
            old_dirty = (page['content'] != page['saved_content'])
            page['content'] = e.args
            new_dirty = (page['content'] != page['saved_content'])
            if old_dirty != new_dirty:
                self.render_tabs()

    def render_tabs(self):
        self.tabs_container.clear()
        with self.tabs_container:
            for page in self.pages:
                is_active = (page['id'] == self.active_page_id)
                bg_color = 'bg-[#08a4e5]/10 dark:bg-[#08a4e5]/20 border-t-2 border-[#08a4e5] text-[#08a4e5] dark:text-[#08a4e5]' if is_active else 'bg-transparent border-t-2 border-transparent text-slate-500 hover:bg-slate-50 dark:hover:bg-slate-800'
                
                with ui.row().classes(f'relative px-3 py-1 cursor-pointer flex items-center gap-2 group/tab transition-colors {bg_color}') as tab_el:
                    def make_switch(pid):
                        return lambda e: self.switch_to_page(pid)
                    tab_el.on('click', make_switch(page['id']))

                    display_name = page['name']
                    if page['content'] != page['saved_content']:
                        display_name += ' *'
                    
                    ui.label(display_name).classes('text-[13px] font-medium whitespace-nowrap select-none')
                    
                    def make_close(pid):
                        return lambda e: self.close_page(pid)
                    close_btn = ui.icon('close').classes('text-[14px] cursor-pointer opacity-0 group-hover/tab:opacity-100 hover:!text-red-500 transition-opacity ml-1')
                    close_btn.on('click.stop', make_close(page['id']))

    def set_content(self, text: str):
        p = self.get_active_page()
        if p and p['path'] is None and p['content'] == p['saved_content']:
            p['content'] = text
            self.editor.value = text
        else:
            self.add_new_page(content=text)

    def update_curr_filename(self, text: str):
        p = self.get_active_page()
        if p:
            p['name'] = text
            self.render_tabs()

    def get_curr_filename(self):
        p = self.get_active_page()
        return p['name'] if p else ""

    def set_file_path(self, path):
        self.current_file_path = path

    def mark_as_saved(self, text: str):
        p = self.get_active_page()
        if p:
            p['saved_content'] = text
            # Ensure the dirty asterisk goes away
            self.render_tabs()

    async def open_save_dialog(self) -> bool:
        with ui.dialog() as dialog, ui.card().classes('w-96 bg-white p-6 rounded-2xl shadow-2xl border border-slate-100'):
            ui.label('Do you want to save?').classes('text-xl font-bold mb-4 text-slate-800 tracking-tight')

            with ui.row().classes('w-full justify-end gap-3 mt-6'):
                ui.button('NO', on_click=lambda: dialog.submit(False)) \
                    .props('flat text-color=grey-7 outline') \
                    .classes('font-medium hover:bg-red-50 hover:text-red-600 rounded-lg')
                ui.button('YES', on_click=lambda: dialog.submit(True)) \
                    .props('color=primary') \
                    .classes('font-bold shadow-sm shadow-[#08a4e5]/20 rounded-lg')

            with ui.row().classes('hidden'):
                # We do not strictly need the extra Close button if they choose Yes/No, keeping original logic.
                ui.button('Close', on_click=dialog.close)

        result = await dialog
        return result