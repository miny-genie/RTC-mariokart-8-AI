import logging
import tkinter as tk
from tkinter import ttk

from playground.ui.widgets import DebounceEntry
from playground.korean_regexp.functions import (
    get_reg_exp as re_korean, eng_to_kor, kor_to_eng
)

logger = logging.getLogger(__name__)


class FiltersFrame(ttk.LabelFrame):
    def __init__(self, parent, play_tab, function_callback=None):
        logger.debug("Initializing Playground FiltersFrame")
        super().__init__(parent, text="Filters")
        self.parent = parent
        self.play_tab = play_tab
        self.function_callback = function_callback
        
        # Name Label
        self.name_label = ttk.Label(self, text="Course Name:")
        self.name_label.grid(row=0, column=0, padx=(5, 0), pady=(5, 5), sticky="w")
        self.name = DebounceEntry(self, width="30")
        self.name_last_seen = ""
        self.name.bind_on_key(self.on_name_key)
        self.name.grid(row=0, column=1, padx=(5, 0), pady=(5, 5), sticky="w")
        
        # Selected Label
        self.selected_label = ttk.Label(self, text="Hint:")
        self.selected_label.grid(row=0, column=2, padx=(5, 0), pady=(5, 5), sticky="w")
        init_text = "한글 검색을 구현 중이니 영문으로 검색해주세요 (예: 빅 블루 > qlr qmffn)"
        self.selected_var = tk.StringVar(value=init_text)
        self.selected_dropdown = ttk.OptionMenu(
            self,
            self.selected_var,
            self.selected_var.get(),
            init_text,
            "맵 이름으로 검색이 가능합니다. (예: 빅 블루)",
            "컵 종류로도 검색이 가능합니다. (예: 젤다 컵)",
            "그랑프리로도 검색이 가능합니다. (예: 니트로 그랑프리)",
            command=self.selected_command,
        )
        self.selected_dropdown.grid(
            row=0, column=3, padx=(5, 0), pady=(5, 5), sticky="w"
        )
        
        # Button
        self.reset_button = ttk.Button(self, text="초기화", command=self.reset_table)
        self.reset_button.grid(row=0, column=4, padx=5, pady=5, sticky="nsew")
        
        # Event Binding
        self.name.bind("<KeyRelease>", self.filter_buttons)
        
    def selected_command(self, _event=None):
        self.play_tab.packs_frame.render_packs()
    
    def on_name_key(self, _event=None):
        name = self.name.get().strip()
        if name != self.name_last_seen:
            self.name_last_seen = name
            self.play_tab.packs_frame.render_packs()
            
    def IME_test(self, event):
        search_term = self.name.get()
        print(search_term)
            
    def filter_buttons(self, event):
        search_term = self.name.get()
        self.function_callback(search_term)
    
    def reset_table(self):
        self.function_callback()