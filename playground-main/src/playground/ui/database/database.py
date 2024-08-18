import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from pandastable import TableModel
import tkinter as tk
from tkinter import ttk

from playground.config import Config
from playground.constants import BASE_DIR
from playground.ui.database.filters import FiltersFrame
from playground.ui.widgets import Tab
from playground.ui.widgets import CustomTable

pd.set_option('future.no_silent_downcasting', True)


class DatabaseTab(Tab):
    def __init__(
        self, tab_control, playground_config: Config, task_manager, *args, **kwargs
    ):
        super().__init__(tab_control, *args, **kwargs)
        self.tab_control = tab_control
        self.playground_config = playground_config
        self.task_manager = task_manager
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        # Top Frame
        self.top_frame = ttk.Frame(self)
        self.top_frame.rowconfigure(0, minsize=60)
        self.top_frame.rowconfigure(1, weight=1)
        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.columnconfigure(1, minsize=250)
        self.top_frame.grid(row=0, column=0, sticky="nsew")
        
        # Search Frame
        self.search_frame = FiltersFrame(
            self.top_frame, play_tab=self, function_callback=self.reset_tab
        )
        self.search_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        # Database Frame
        self.database_frame = ttk.LabelFrame(self.top_frame, text="Database")
        self.database_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        # Load Database
        current_path = BASE_DIR / "ui" / "database"
        self.origin_csv = pd.read_csv(current_path / "train_data.csv")
        self.database = CustomTable(
            tab=self,
            parent=self.database_frame,
            dataframe=self.origin_csv.copy(),
            showtoolbar=False,
            showstatusbar=False,
        )
        self.database.grid(row=0, column=0, sticky="nsew")
        self.database.show()
        
        # Graph Frame
        self.graph_frame = ttk.Frame(self.top_frame)
        self.graph_frame.rowconfigure(0, weight=1)
        self.graph_frame.rowconfigure(1, weight=1)
        self.graph_frame.rowconfigure(2, weight=1)
        self.graph_frame.columnconfigure(0, weight=1)
        self.graph_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")
        
        # test
        self.graph1 = ttk.LabelFrame(self.graph_frame, text="test")
        self.graph1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.graph2 = ttk.LabelFrame(self.graph_frame, text="test")
        self.graph2.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.graph3 = ttk.LabelFrame(self.graph_frame, text="test")
        self.graph3.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
    
    def reset_tab(self):
        try:
            self.graph1.winfo_children()[0].destroy()
            self.graph2.winfo_children()[0].destroy()
            self.graph3.winfo_children()[0].destroy()
        except IndexError:
            pass
        self.database.updateModel(TableModel(self.origin_csv.copy()))
        self.database.redraw()
    
    def draw_pie_chart(self, value):
        
        return
    
    def _draw_pie_chart(self, value):
        # print(value, "RIGHT WAY")
        fig = plt.Figure(figsize=(2, 2), dpi=100)
        ax = fig.add_subplot(111)
        data = [int(value), 100 - int(value)]  # 예시 데이터
        # labels = ['Selected Value', 'Others']
        ax.pie(data, autopct='%1.1f%%')

        # 이전 그래프 삭제
        for widget in self.graph1.winfo_children():
            widget.destroy()

        # 그래프를 tkinter 위젯에 배치
        canvas = FigureCanvasTkAgg(fig, master=self.graph1)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 이전 그래프 삭제
        for widget in self.graph2.winfo_children():
            widget.destroy()

        # 그래프를 tkinter 위젯에 배치
        canvas = FigureCanvasTkAgg(fig, master=self.graph2)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 이전 그래프 삭제
        for widget in self.graph3.winfo_children():
            widget.destroy()

        # 그래프를 tkinter 위젯에 배치
        canvas = FigureCanvasTkAgg(fig, master=self.graph3)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)