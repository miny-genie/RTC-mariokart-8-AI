import logging
import sys
import threading
import time
import tkinter as tk
import traceback
from tkinter import PhotoImage, ttk
from multiprocessing import Queue
from pathlib import Path
from PIL import Image, ImageTk

from playground.constants import BASE_DIR, IS_EXE
from playground.updater import self_update
from playground.version import current_version, latest_version
from playground.config import Config, MIN_WIDTH, MIN_HEIGHT
from playground.utils import tb_info, temp_chdir

from playground.ui.database import DatabaseTab
from playground.ui.error import ErrorTab
# from playground.ui.extract import ExtractTab
from playground.ui.logs import QueueHandler, register_queue_handler
from playground.ui.personal import PersonalTab
from playground.ui.play import PlayTab
from playground.ui.settings import SettingsTab
from playground.ui.tasks import TaskManager, PING_INTERVAL
from playground.ui.trackers import TrackersTab
from playground.ui.widgets import ConsoleWindow


logger = logging.getLogger(__name__)
update_lock = threading.Lock()


TAB_KEYS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]


def exception_logger(type_, value, traceb):
    exc = traceback.format_exception(type_, value, traceb)
    logger.critical(f"unhandled Exception: {''.join(exc).strip()}")
    
    
def update_start(_call, launcher_exe):
    self_update(launcher_exe)
    
    
def check_for_latest(call):
    logger.debug("Checking for latest Playground version.")
    acquired = update_lock.acquire(blocking=False)
    if not acquired:
        logger.warning(
            "Attempted to check for new Playground while another task is running."
        )
        return
    
    playground_latest_version = None
    try:
        playground_latest_version = latest_version()
    finally:
        update_lock.release()
        
    call("playground:latest_version", playground_latest_version=playground_latest_version)


class PlaygroundUI:
    CHECK_LATEST_INTERVAL = 1000 * 30 * 60    # 30 minutes
    
    def __init__(self, playground_config: Config, log_level=logging.INFO):
        logger.debug("Initializing UI")
        self.playground_config = playground_config
        
        self.current_version = current_version()
        self.latest_version = None
        self.needs_update = False
        
        self._shutdown_handlers = []
        self._shutting_down = False
        
        self.log_queue = Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        register_queue_handler(self.queue_handler, log_level)
        self.task_manager = TaskManager(self.log_queue, log_level)
        self.task_manager.register_task(
            "playgruond:update_start",
            update_start,
            True,
            on_complete="playground:update_complete",
        )
        self.task_manager.register_handler(
            "playground:update_complete", self.update_complete
        )
        self.task_manager.register_task(
            "playground:check_for_latest",
            check_for_latest,
            True,
        )
        self.task_manager.register_handler(
            "playground:latest_version", self.handle_playground_latest_version
        )
        
        self.root = tk.Tk(className="Playground")
        
        self.load_themes()
        style = ttk.Style(self.root)
        self.root.default_theme = style.theme_use()
        valid_themes = self.root.call("ttk::themes")
        
        self.root.title("Playground")
        self.root.geometry(playground_config.geometry)
        self.last_geometry = playground_config.geometry
        self.root.bind("<Configure>", self.handle_resize)
        if playground_config.theme and playground_config.theme in valid_themes:
            style.theme_use(playground_config.theme)
        self.root.event_add("<<ThemeChange>>", "None")
        
        style.configure(
            "ModList.TCheckbutton",
            font=("Segoe UI", 12, "bold"),
            # TODO: dynamic sizing for larger windows
            wraplength="640",
        )
        style.configure("Update.TButton", font="sans 12 bold")
        style.configure("TOptionMenu", anchor="w")
        style.configure("Link.TLabel", foreground="royal blue")
        style.configure(
            "Thicc.TButton",
            font=("Arial", 16, "bold"),
        )
        
        default_background = style.lookup("TFrame", "background")
        self.root.configure(bg=default_background)
        
        self.root.minsize(MIN_WIDTH, MIN_HEIGHT)
        self.icon_png = PhotoImage(file=BASE_DIR / "static/images/icon.png")
        self.root.iconphoto(False, self.icon_png)
        
        sys.excepthook = exception_logger
        self.root.report_callback_exception = exception_logger
        
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        self.top_frame = ttk.Frame(self.root)
        self.top_frame.grid(row=0, column=0, sticky="nsew")
        
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_rowconfigure(0, weight=0)
        self.top_frame.grid_rowconfigure(1, weight=1)
        self.top_frame.grid_rowconfigure(2, weight=0)
        
        self.update_frame = ttk.LabelFrame(
            self.top_frame, text="Playground Update Available"
        )
        self.update_frame.columnconfigure(0, weight=1)
        self.update_frame.rowconfigure(0, weight=1)
        
        self.update_button = ttk.Button(
            self.update_frame,
            text="Update Now!",
            command=self.update,
            style="Update.TButton",
        )
        
        # Handle shutting down cleanly
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.root.bind("<Escape>", self.quit)
        
        self.tabs = {}
        self.tab_control = ttk.Notebook(self.top_frame)
        
        logger.debug("Registering Tabs")      
        self.register_tab(
            "불안전한 놀이터 ",
            PlayTab,
            tab_control=self.tab_control,
            playground_config=playground_config,
            task_manager=self.task_manager,
            tabs = self.tabs,
        )
        self.register_tab(
            "사관 데이터 ",
            DatabaseTab,
            tab_control=self.tab_control,
            playground_config=playground_config,
            task_manager=self.task_manager,
        )
        self.register_tab(
            "개인 투자 기록 ",
            PersonalTab,
            tab_control=self.tab_control,
            playground_config=playground_config,
            task_manager=self.task_manager,
        )
        # self.tabs["불안전한 놀이터 "].set_personal_tab(self.tabs["개인 투자 기록 "])
        self.register_tab(
            "투자 성향 ",
            TrackersTab,
            tab_control=self.tab_control,
            playground_config=playground_config,
            task_manager=self.task_manager,
        )
        self.register_tab(
            "설정 ",
            SettingsTab,
            tab_control=self.tab_control,
            playground_config=playground_config,
        )
        
        # if not playground_config.install_dir:
        #     logger.critical(
        #         "Must go to the Settings and set the Install Directory to use playground."
        #     )
        #     for i in range(0, 5):
        #         self.tab_control.tab(i, state="disabled")
        
        # Keycode for Playground UI drawing
        self.select_last_tab()
        self.tab_control.bind("<<NotebookTabChanged>>", self.on_tab_change)
        self.tab_control.grid(column=0, row=1, padx=2, pady=(4, 0), sticky="nsew")
        
        self.console_frame = ttk.LabelFrame(self.top_frame, text="Console")
        self.console_frame.columnconfigure(0, weight=1)
        self.console_frame.rowconfigure(0, weight=1)
        
        self.console = ConsoleWindow(self.queue_handler, self.console_frame)
        self.console.grid(column=0, row=0, padx=2, pady=2, sticky="ew")

        self.version_label = ttk.Label(
            self.top_frame,
            text=f"v{self.current_version}",
            font="Helvetica 9 italic",
        )
        self.version_label.grid(column=0, row=3, padx=5, sticky="e")
        
        self.ws_thread = None
        #  self.task_manager.start_process()
        self.last_ping = time.time()
        # self.root.after(100, self.after_task_manager)
        # self.root.after(1000, self.after_ws_thread)
        # self.root.after(1000, self.after_record_win)
        self.check_for_updates()
        # self.check_requirments()
        
    def check_for_updates(self):
        if self.needs_update:
            return
        
        self.task_manager.call("playground:check_for_latest")
        self.root.after(self.CHECK_LATEST_INTERVAL, self.check_for_updates)
    
    @staticmethod
    def check_requirments():
        return
    
    def handle_playground_latest_version(self, playground_latest_version):
        if not IS_EXE:
            return
    
    def after_ws_thread():
        return
    
    def after_record_win():
        return
    
    def after_task_manager(self):
        if not self.task_manager.is_alive():
            # Worker process went away, but shutting down so just return.
            if self._shutting_down:
                return
            
            # Worker process went away unexpectedly, Restart it.
            logger.critical("Worker process went away, Restarting it.")
            self.task_manager.start_process()
            self.root.after(100, self.after_task_manager)
            
        # Send regular pings so the worker process knows.
        now = time.time()
        if now - self.last_ping > PING_INTERVAL:
            self.last_ping = now
            self.task_manager.ping()
            
        while True:
            msg = self.task_manager.receive_message()
            if msg is None:
                self.root.after(100, self.after_task_manager)
                return
            
            self.root.after_idle(self.task_manager.dispatch, msg)
    
    def handle_resize(self, event):
        if not isinstance(event.widget, tk.Tk):
            return
        self.last_geometry = self.root.geometry()
    
    def update(self):
        return
    
    def update_complete(self):
        self.quit()
    
    def register_shutdown_handler(self, func):
        self._shutdown_handlers.append(func)
    
    def select_last_tab(self):
        last_tab = self.tabs.get(self.playground_config.last_tab)
        if last_tab is None:
            return
        self.tab_control.select(last_tab)
        
    def on_tab_change(self, event):
        tab_name = event.widget.tab("current")["text"]
        tab = self.tabs[tab_name]
        if tab.show_console:
            self.render_console()
        else:
            self.forget_console()
            
        self.playground_config.last_tab = tab_name
        self.playground_config.save()
        tab.on_load()
    
    def render_console(self):
        self.console_frame.grid(row=2, column=0, padx=5, pady=(5, 0), sticky="nswe")
    
    def forget_console(self):
        self.console_frame.grid_forget()
    
    def register_tab(self, name, cls, **kwargs):
        logger.debug("Registering Tab %s", repr(name))
        
        try:
            obj = cls(**kwargs)
        except Exception:
            obj = ErrorTab(tab_control=self.tab_control)
            logger.critical("Failed to register tab %s: %s", name, tb_info())
            
        num_tabs = len(self.tabs)
        if num_tabs < len(TAB_KEYS):
            self.root.bind(
                f"<Control-Key-{TAB_KEYS[num_tabs]}>",
                lambda _: self.tab_control.select(obj),
            )
            
        self.tabs[name] = obj
        self.tab_control.add(obj, text=name)
    
    def tabs_needing_save(self):
        needs_save = []
        for tab_name, tab in self.tabs.items():
            if tab.save_needed:
                needs_save.append(tab_name)
        return needs_save
    
    def should_close(self, needs_save):
        tabs = ", ".join(needs_save)
        msg_box = tk.messagebox.askquestion(
            "Close Playground?",
            (
                f"You have some tabs ({tabs}) with unsaved changes.\n"
                "Are you sure you want to exit without saving?"
            ),
            icon="warning"
        )
        return msg_box == "yes"
    
    def quit(self, _event=None):
        if self._shutting_down:
            return
        
        needs_save = self.tabs_needing_save()
        should_close = True
        if needs_save:
            should_close = self.should_close(needs_save)
            
        if not should_close:
            return
        
        self._shutting_down = True
        logger.info("Shutting down.")
        for handler in self._shutdown_handlers:
            handler()
            
        self.task_manager.quit()
        self.root.quit()
        self.root.destroy()
        
    def load_themes(self):
        static_dir = BASE_DIR / "static"
        themes_dir = static_dir / "themes"
        with temp_chdir(static_dir):
            self.root.call("lappend", "auto_path", f"[{themes_dir}]")
            self.root.eval("source themes/pkgIndex.tcl")
        
    def mainloop(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.quit()


config = Config()
window = PlaygroundUI(config)
window.mainloop()