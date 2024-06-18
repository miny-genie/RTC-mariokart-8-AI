import logging
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk
from tkinter import ttk

from playground.constants import BASE_DIR
from playground.config import Config, MIN_WIDTH, MIN_HEIGHT
from playground.utils import is_windows
if is_windows():
    import winshell

from playground.ui.database.constants import COURSE_NAMING
from playground.korean_regexp.functions import (
    get_reg_exp as re_korean, eng_to_kor, kor_to_eng
)


logger = logging.getLogger(__name__)


class CourseFrame(ttk.Frame):
    def __init__(self, parent, play_tab, playground_config: Config):
        logger.debug("Initializing Playground CourseFrame.")
        super().__init__(parent)
        self.parent = parent
        self.play_tab = play_tab
        self.playground_config = playground_config
        
        # declaration variables
        self.weight = 0.85
        self.image_width = int(MIN_WIDTH // 3 * 2 // 4 * self.weight)
        self.image_height = int(MIN_HEIGHT * self.image_width // MIN_WIDTH)
        self.course_images = [None]
        self.course_buttons = [None]
        self.course_labels = [None]
        self.is_visible = [False] * (96+1)
        # self.button_name = [None]
        
        # Add images
        for i in range(1, 96+1):
            image = self.load_image(i, self.image_width, self.image_height)
            self.course_images.append(image)

        # Add buttons
        for row in range(24):
            for col in range(4):
                image_num = row * 4 + col + 1
                button = tk.Button(
                    self.parent,
                    image=self.course_images[image_num],
                    text=str(image_num),
                    command=lambda img_num = image_num: self.launch(img_num),
                )
                button.grid(
                    row=row * 2,
                    column=col,
                    padx=1,
                    pady=1,
                    sticky="nswe"
                )
                
                png_name = "course" + str(image_num).zfill(3) + ".png"
                course_name = COURSE_NAMING[png_name][4]
                label = tk.Label(self.parent, text=course_name)
                label.grid(
                    row=row * 2 + 1,
                    column=col,
                    padx=1,
                    pady=1,
                    sticky="nswe"
                )
                
                self.course_buttons.append(button)
                self.course_labels.append(label)
                self.is_visible[image_num] = True
                # self.button_name.append(self.image_naming(image_num))
        
    def image_naming(self, num):
        return f"course{num:03}.png"
    
    def load_image(self, num, width, height):
        image_name = self.image_naming(num)
        image_path = BASE_DIR / "static" / "images"
        return ImageTk.PhotoImage(
            Image.open(image_path / image_name).resize(
                (width, height), Image.Resampling.LANCZOS
            )
        )
        
    def update_grid(self):
        visuality = [
            (btn, label)
            for visible, btn, label in zip(self.is_visible, self.course_buttons, self.course_labels)
            if visible
        ]
        
        for idx, (btn, lbl) in enumerate(visuality):
            row = idx // 4
            col = idx % 4
            btn.grid(row=row*2, column=col, padx=1, pady=1, sticky="nswe")
            lbl.grid(row=row*2+1, column=col, padx=1, pady=1, sticky="nswe")
    
    def launch(self, img_num):
        self.play_tab.course.delete(0, tk.END)
        self.play_tab.course.insert(0, img_num)
        # self.course_buttons[img_num].grid_remove()
        # self.is_visible[img_num] = False
        self.update_grid()
        
    def filter_buttons(self, search_term):
        def isENG(text: str) -> bool:
            return ''.join(text.split()).encode().isalnum()
        
        def convert(text: str) -> str:
            return ''.join(text.split()).lower()
        
        # name = [grandprix_KOR, grandprix_ENG, cup_KOR, cup_ENG, track_KOR, track_ENG]
        # kor_idx, eng_idx = [0, 2, 4], [1, 3, 5]
        
        search_term = search_term.lower()
        for idx, (_, names) in enumerate(COURSE_NAMING.items(), 1):
            for name in names:
                if isENG(name) and convert(search_term) in convert(name):
                    self.is_visible[idx] = True
                    self.course_buttons[idx].grid()
                    self.course_labels[idx].grid()
                    break
            else:
                self.is_visible[idx] = False
                self.course_buttons[idx].grid_remove()
                self.course_labels[idx].grid_remove()
        
        self.update_grid()