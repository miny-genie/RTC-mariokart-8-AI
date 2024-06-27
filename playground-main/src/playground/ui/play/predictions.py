import customtkinter as ctk
import logging
import tkinter as tk
from tkinter import ttk

logger = logging.getLogger(__name__)


class FirstPredictionFrame(ttk.LabelFrame):
    def __init__(self, parent):
        logger.debug("Initializing Playground FirstPredictionFrame")
        super().__init__(parent, text="Track 1")
        self.parent = parent
        
        # Style config
        self.style = ttk.Style()
        self.style.configure("size10.TLabel", font=("맑은 고딕", 10))
        
        # self.rowconfigure()
        self.columnconfigure(0, weight=1)
        
        # Course Info
        self.course_label = ttk.Label(
            self, text="맵 이름", style="size10.TLabel", anchor="center"
        )
        self.course_label.grid(column=0, padx=5, pady=5, sticky="we")
        self.course = ttk.Entry(self, width=25)
        self.course.grid()
        
        # N판
        self.game_count_label = ttk.Label(
            self, text="0판", style="size10.TLabel", anchor="center"
        )
        self.game_count_label.grid(column=0, padx=5, pady=5, sticky="we")
        self.game_count = ctk.CTkSlider(
            self, from_=1, to=5, number_of_steps=5,
            command=self.update_game_count_label
        )
        self.game_count.grid(column=0, padx=5, pady=5, sticky="nswe")
        
        # 합계 R등 이내
        self.game_goal_label = ttk.Label(
            self, text="합계 0등 이내", style="size10.TLabel", anchor="center"
        )
        self.game_goal_label.grid(column=0, padx=5, pady=5, sticky="we")
        self.game_goal = ctk.CTkSlider(
            self, from_=1, to=25, number_of_steps=25,
            command=self.update_game_goal_label
        )
        self.game_goal.grid(column=0, padx=5, pady=5, sticky="nswe")
        
        # track cc
        self.tmp_label = ttk.Label(
            self, text="cc", style="size10.TLabel", anchor="center"
        )
        self.tmp_label.grid(column=0, padx=5, pady=5, sticky="we")
        self.tmp = ctk.CTkSlider(
            self, from_=1, to=25, number_of_steps=25,
            command=self.update_tmp
        )
        self.tmp.grid(column=0, padx=5, pady=5, sticky="nswe")
        
        # 참가 인원
        self.tmp_label = ttk.Label(
            self, text="참가 인원", style="size10.TLabel", anchor="center"
        )
        self.tmp_label.grid(column=0, padx=5, pady=5, sticky="we")
        self.tmp = ctk.CTkSlider(
            self, from_=1, to=25, number_of_steps=25,
            command=self.update_tmp
        )
        self.tmp.grid(column=0, padx=5, pady=5, sticky="nswe")
        
    def update_game_count_label(self, value):
        self.game_count_label.config(text=f"{str(int(value))}판")
    
    def update_game_goal_label(self, value):
        self.game_goal_label.config(text=f"합계 {str(int(value))}등 이내")
    
    def update_tmp(self, value):
        return


class SecondPredictionFrame(ttk.LabelFrame):
    def __init__(self, parent):
        logger.debug("Initializing Playground SecondPredictionFrame")
        super().__init__(parent, text="Track 2")
        self.parent = parent
        
        # # Course Info
        # self.course_label2 = ttk.Label(self.predict_frame2, text="맵 이름: ")
        # self.course_label2.grid(sticky="nswe")
        # self.course2 = ttk.Entry(self.predict_frame2, width=25)
        # self.course2.grid()