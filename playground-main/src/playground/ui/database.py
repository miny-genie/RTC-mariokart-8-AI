import tkinter as tk
from tkinter import ttk

from playground.config import Config
from playground.ui.widgets import Tab


class DatabaseTab(Tab):
    def __init__(
        self, tab_control, playground_config: Config, task_manager, *args, **kwargs
    ):
        super().__init__(tab_control, *args, **kwargs)
        self.tab_control = tab_control
        self.playground_config = playground_config
        self.task_manager = task_manager
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        
        # self.fyi_install
        # self.fyi_install
        
        sep = ttk.Separator(self, orient=tk.VERTICAL)
        sep.grid(row=0, column=1, padx=10, sticky="ns")
        
        # self.local_install
        # self.local_install.grid()
        
    def on_load(self):
        self.render()
        
    def render(self):
        # self.fyi_install.render()
        # self.local_install.render()
        return