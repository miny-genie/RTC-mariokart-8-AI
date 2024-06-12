import logging
import tkinter as tk
from tkinter import ttk

from playground.ui.widgets import DebounceEntry


logger = logging.getLogger(__name__)


class FiltersFrame(ttk.LabelFrame):
    def __init__(self, parent, play_tab, function_callback=None):
        logger.debug("Initailizing Playground FiltersFrame")
        super().__init__(parent, text="Filters")
        self.parent = parent
        self.play_tab = play_tab
        self.function_callback = function_callback
        
        self.name_label = ttk.Label(self, text="Course Name:")
        self.name_label.grid(row=0, column=0, padx=(5, 0), pady=(5, 5), sticky="w")
        self.name = DebounceEntry(self, width="30")
        self.name_last_seen = ""
        self.name.bind_on_key(self.on_name_key)
        self.name.grid(row=0, column=1, padx=(5, 0), pady=(5, 5), sticky="w")
        
        self.selected_label = ttk.Label(self, text="Hint:")
        self.selected_label.grid(row=0, column=2, padx=(5, 0), pady=(5, 5), sticky="w")
        self.selected_var = tk.StringVar(value="검색 힌트보기")
        self.selected_dropdown = ttk.OptionMenu(
            self,
            self.selected_var,
            self.selected_var.get(),
            "검색 힌트보기",
            "맵 이름으로 검색이 가능합니다.",
            "컵 이름으로도 검색이 가능합니다.",
            "이스터에그도 있습니다. (ex:개블루)",
            command=self.selected_command,
        )
        self.selected_dropdown.grid(
            row=0, column=3, padx=(5, 0), pady=(5, 5), sticky="w"
        )
        
        self.name.bind("<KeyRelease>", self.filter_buttons)
        
    def selected_command(self, _event=None):
        self.play_tab.packs_frame.render_packs()
    
    def on_name_key(self, _event=None):
        name = self.name.get().strip()
        if name != self.name_last_seen:
            self.name_last_seen = name
            self.play_tab.packs_frame.render_packs()
            
    def filter_buttons(self, event):
        search_term = self.name.get()
        self.function_callback(search_term)