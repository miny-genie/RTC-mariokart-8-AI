import logging
import tkinter as tk
from tkinter import ttk

from playground.config import Config
from playground.ui.widgets import Tab

logger = logging.getLogger(__name__)


class SettingsTab(Tab):
    def __init__(self, tab_control, playground_config: Config, *args, **kwargs):
        super().__init__(tab_control, *args, **kwargs)
        self.tab_control = tab_control
        self.playground_config = playground_config
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)