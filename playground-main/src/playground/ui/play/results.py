import logging
import tkinter as tk
from tkinter import ttk

logger = logging.getLogger(__name__)


class ResultFrame(ttk.LabelFrame):
    def __init__(self, parent):
        logger.debug("Initializing Playground ResultFrame")
        super().__init__(parent, text="Result")
        self.parent = parent
        
        # Style config
        self.style = ttk.Style()
        self.style.configure("Bold.TLabel", font=("맑은 고딕", 12, "bold"))
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, minsize=20)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, minsize=20)
        
        self.success_label = ttk.Label(self, text="성공 여부", style="Bold.TLabel")
        self.success_label.grid(row=0, column=1, padx=5, sticky="se")
        
        self.success_probability = ttk.Label(self, text="00.00%", style="Bold.TLabel")
        self.success_probability.grid(row=0, column=2, padx=5, sticky="sw")
        
        self.rank_label = ttk.Label(self, text="등수 예측", style="Bold.TLabel")
        self.rank_label.grid(row=1, column=1, padx=5, pady=5, sticky="ne")
        
        self.rank_probability = ttk.Label(self, text="00위", style="Bold.TLabel")
        self.rank_probability.grid(row=1, column=2, padx=5, pady=5, sticky="nw")