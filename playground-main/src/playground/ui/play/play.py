import joblib
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.decomposition import PCA
import tkinter as tk
from tkinter import ttk

from playground.config import Config
from playground.constants import BASE_DIR
from playground.ui.database.constants import COURSE_TO_ENCODE, COURSE_NAMING
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
        self.track_1_reg_model = self.load_model(version="reg", track=1)
        self.track_1_clf_model = self.load_model(version="clf", track=1)
        self.pca = self.load_model(version="pca")
        
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
        self.button_play = ttk.Button(self, text="불안전한 놀이터!", command=self.predict)
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
    
    def load_model(self, version: str, track: int = 0) -> BaseEstimator:
        model_path = BASE_DIR / "static" / "models"
        if version == "pca":
            loaded_file = f"pca.pkl"
        else:
            loaded_file = f"track_{track}_{version}_model.pkl"
        loaded_model = joblib.load(model_path / loaded_file)
        return loaded_model
    
    def filter_buttons(self, search_term):
        self.course_frame.filter_buttons(search_term)
    
    ''' 이 부분 label-encoding 번호 일치시키기 '''
    ''' One-Hot Encoding 바꿔서 pca.fit_transform 다시 하고, [0] * 96으로 '''
    def predict(self) -> None:
        course = self.predict_frame.course_entry.get()
        for names in COURSE_NAMING.values():
            if course in names:
                encode = COURSE_TO_ENCODE[names[5]]
        
        data = [False] * 91
        data[encode] = True
        pca_transfrom = self.pca.transform(pd.DataFrame(data).T)[0]
        
        game_count = int(self.predict_frame.game_count.get())
        game_goal = int(self.predict_frame.game_goal.get())
        cur_game_count = 1
        cc = int(self.predict_frame.cc.get())
        part_people = int(self.predict_frame.part_people.get())
        pre_data = [game_count, game_goal, cur_game_count, cc, part_people]
        dummy = [pre_data + list(pca_transfrom)]

        reg_result = self.track_1_reg_model.predict(dummy)
        clf_result = self.track_1_clf_model.predict(dummy)
        
        self.result_frame.success_probability.config(
            text=f"{clf_result}"
        )
        self.result_frame.rank_probability.config(
            text=f"{reg_result}"
        )
        return