import tkinter as tk
from tkinter import ttk

from playground.config import Config
from playground.ui.play.courses import CourseFrame
from playground.ui.play.filters import FiltersFrame
from playground.ui.play.predictions import FirstPredictionFrame, SecondPredictionFrame
from playground.ui.play.results import ResultFrame
from playground.ui.widgets import ScrollableFrameLegacy, Tab


class PlayTab(Tab):
    def __init__(
        self, tab_control, playground_config: Config, task_manager, *args, **kwargs
    ):
        super().__init__(tab_control, *args, **kwargs)
        self.tab_control = tab_control
        self.playground_config = playground_config
        self.task_manager = task_manager
        
        # Configure
        self.rowconfigure(0, minsize=200)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, minsize=100)
        self.rowconfigure(3, minsize=60)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, minsize=240)
        self.columnconfigure(2, minsize=240)
        
        # Left Root Frame
        self.play_wrapper = ttk.Frame(self)
        self.play_wrapper.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.play_wrapper.columnconfigure(0, weight=1)
        self.play_wrapper.rowconfigure(1, weight=1)
        
        # Filters Frame
        self.filter_frame = FiltersFrame(
            self.play_wrapper, play_tab=self, function_callback=self.filter_buttons
        )
        self.filter_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        # Course Frame
        self.scrollable_course_frame = ScrollableFrameLegacy(
            self.play_wrapper, text="Course"
        )
        self.scrollable_course_frame.grid(
            row=1, column=0, padx=5, pady=5, sticky="nsew"
        )
        self.course_frame = CourseFrame(
            self.scrollable_course_frame.scrollable_frame, self, playground_config
        )
        self.course_frame.grid(row=1, column=0, sticky="nsew")
        
        # Track 1: Predictions Frame
        self.predict_frame = FirstPredictionFrame(self)
        self.predict_frame.grid(
            row=0, column=1, rowspan=2, padx=5, pady=5, sticky="nsew"
        )
        
        # Track 1: Result Frame
        self.result_frame = ResultFrame(self)
        self.result_frame.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
                
        # Track 1: Button
        self.button_play = ttk.Button(self, text="불안전한 놀이터!")
        self.button_play.grid(row=3, column=1, pady=5, padx=5, sticky="nswe")
        
        # Track 2: Predictions Frame
        self.predict_frame2 = SecondPredictionFrame(self)
        self.predict_frame2.grid(
            row=0, column=2, rowspan=2, padx=5, pady=5, sticky="nsew"
        )
        
        # Track 2: Result Frame
        self.result_frame2 = ResultFrame(self)
        self.result_frame2.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")
                
        # Track 2: Button
        self.button_play2 = ttk.Button(self, text="불안전한 놀이터!")
        self.button_play2.grid(row=3, column=2, pady=5, padx=5, sticky="nswe")
        
    def filter_buttons(self, search_term):
        self.course_frame.filter_buttons(search_term)
    
    def predict(self):
        return