import logging
import tkinter as tk
from tkinter import ttk

from playground.config import Config
from playground.ui.widgets import Tab

logger = logging.getLogger(__name__)


class PersonalTab(Tab):
    def __init__(self, tab_control, playground_config: Config, task_manager, *args, **kwargs):
        super().__init__(tab_control, *args, **kwargs)
        self.tab_control = tab_control
        self.playground_config = playground_config
        self.task_manager = task_manager
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        # Root Frame
        self.play_wrapper = ttk.Frame(self)
        self.play_wrapper.grid(row=0, column=0, sticky="nsew")
        
        self.temp = ttk.Label(self.play_wrapper, text="temp")
        self.temp.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        