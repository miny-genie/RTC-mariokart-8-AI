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
        self.course_frame = ttk.Frame(self)
        self.course_frame.grid(column=0, padx=5, pady=5, sticky="we")
        self.course_frame.rowconfigure(0, weight=1)
        self.course_frame.columnconfigure(0, weight=1)
        self.course_frame.columnconfigure(1, weight=1)
        
        self.course_label = ttk.Label(
            self.course_frame, text="맵 이름", style="size10.TLabel", anchor="center"
        )
        self.course_label.grid(row=0, column=0, padx=5, pady=5,)
        
        self.course_remove_btn = ttk.Button(
            self.course_frame, text="지우기", command=self.clear_entry
        )
        self.course_remove_btn.grid(row=0, column=1, padx=5, pady=5, sticky="we")
        
        # Course Entry
        self.course_entry = ttk.Entry(self, width=25)
        self.course_entry.grid(column=0, padx=5, pady=5, sticky="we")
        
        # N판
        self.game_count_label = ttk.Label(
            self, text="0판", style="size10.TLabel", anchor="center"
        )
        self.game_count_label.grid(column=0, padx=5, pady=5, sticky="we")
        self.game_count = ctk.CTkSlider(
            self, from_=1, to=5, number_of_steps=4,
            command=self.update_game_count_label
        )
        self.game_count.grid(column=0, padx=5, pady=5, sticky="nswe")
        
        # 합계 R등 이내
        self.game_goal_label = ttk.Label(
            self, text="합계 0등 이내", style="size10.TLabel", anchor="center"
        )
        self.game_goal_label.grid(column=0, padx=5, pady=5, sticky="we")
        self.game_goal = ctk.CTkSlider(
            self, from_=1, to=25, number_of_steps=24,
            command=self.update_game_goal_label
        )
        self.game_goal.grid(column=0, padx=5, pady=5, sticky="nswe")
        
        # track cc
        self.cc_label = ttk.Label(
            self, text="cc", style="size10.TLabel", anchor="center"
        )
        self.cc_label.grid(column=0, padx=5, pady=5, sticky="we")
        self.cc = ctk.CTkSlider(
            self, from_=1, to=4, number_of_steps=3,
            command=self.update_track_cc_label
        )
        self.cc.grid(column=0, padx=5, pady=5, sticky="nswe")
        
        # 참가 인원
        self.part_people_label = ttk.Label(
            self, text="참가 인원 00명", style="size10.TLabel", anchor="center"
        )
        self.part_people_label.grid(column=0, padx=5, pady=5, sticky="we")
        self.part_people = ctk.CTkSlider(
            self, from_=1, to=12, number_of_steps=11,
            command=self.update_part_people
        )
        self.part_people.grid(column=0, padx=5, pady=5, sticky="nswe")
        
    def update_game_count_label(self, value):
        self.game_count_label.config(text=f"{str(int(value))}판")
    
    def update_game_goal_label(self, value):
        self.game_goal_label.config(text=f"합계 {str(int(value))}등 이내")
    
    def update_track_cc_label(self, value):
        tmp_trans = {1:"100cc", 2:"150cc", 3:"200cc", 4:"mirror"}
        self.cc_label.config(text=tmp_trans[int(value)])
    
    def update_part_people(self, value):
        self.part_people_label.config(text=f"참가 인원 {str(int(value)).zfill(2)}명")
    
    def clear_entry(self):
        self.course_entry.delete(0, tk.END)


class SecondPredictionFrame(FirstPredictionFrame):
    def __init__(self, parent):
        logger.debug("Initializing Playground SecondPredictionFrame")
        super().__init__(parent)
        self.config(text="Track 2")
        self.parent = parent
        
        # # Course Info
        # self.course_label2 = ttk.Label(self.predict_frame2, text="맵 이름: ")
        # self.course_label2.grid(sticky="nswe")
        # self.course2 = ttk.Entry(self.predict_frame2, width=25)
        # self.course2.grid()