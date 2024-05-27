import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from playground.config import Config, MIN_WIDTH, MIN_HEIGHT
from playground.constants import BASE_DIR
from playground.ui.widgets import ScrollableFrameLegacy, Tab
from playground.ui.play.filters import FiltersFrame


class PlayTab(Tab):
    def __init__(
        self, tab_control, playground_config: Config, task_manager, *args, **kwargs
    ):
        super().__init__(tab_control, *args, **kwargs)
        self.tab_control = tab_control
        self.playground_config = playground_config
        self.task_manager = task_manager
        
        # declaration variables
        common_padx = 1
        common_pady = 1
        self.weight = 0.85
        self.image_width = int(MIN_WIDTH // 3 * 2 // 4 * self.weight)
        self.image_height = int(MIN_HEIGHT * self.image_width // MIN_WIDTH)
        self.course_images = [None]
        self.course_buttons = [None]
        
        # Configure
        self.rowconfigure(0, minsize=200)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, minsize=20)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, minsize=250)
        self.columnconfigure(2, minsize=250)
        
        # Left Root Frame
        self.play_wrapper = ttk.Frame(self)
        self.play_wrapper.grid(row=0, column=0, rowspan=3, sticky="nsew")
        self.play_wrapper.columnconfigure(0, weight=1)
        self.play_wrapper.rowconfigure(1, weight=1)
        
        # Filters Frame
        self.filter_frame = FiltersFrame(self.play_wrapper, play_tab=self)
        self.filter_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        # Course Frame
        self.scrollable_course_frame = ScrollableFrameLegacy(
            self.play_wrapper, text="Course"
        )
        self.scrollable_course_frame.grid(
            row=1, column=0, columnspan=2, padx=5, pady=0, sticky="nsew"
        )
        self.course_frame = ttk.Frame(
            self.scrollable_course_frame.scrollable_frame
        )
        self.course_frame.grid(row=1, column=0, sticky="nsew")
        
        # Unsafe Playground Frame
        self.right_frame = ttk.Frame(self)
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        
        # Play Button
        self.button_play = ttk.Button(
            self.right_frame, text="불안전한 놀이터!",
        )
        self.button_play.grid(row=0, column=0, pady=5, padx=5, sticky="swe")
        
        # Course Info
        self.course_label = ttk.Label(self.right_frame, text="맵 이름: ")
        self.course_label.grid()
        self.course = ttk.Entry(self.right_frame, width=30)
        self.course.grid()
        
        # Add images
        for i in range(1, 96+1):
            image = self.load_image(i, self.image_width, self.image_height)
            self.course_images.append(image)

        # Add buttons
        for row in range(24):
            for col in range(4):
                image_num = row * 4 + col + 1
                button = tk.Button(
                    self.course_frame,
                    image=self.course_images[image_num],
                    text=str(image_num),
                    command=lambda img_num = image_num: self.launch(img_num),
                )
                button.grid(
                    row=row,
                    column=col,
                    padx=common_padx,
                    pady=common_pady,
                    sticky="nswe"
                )
                self.course_buttons.append(button)
                
        # for i in range(24):
        #     self.left_frame.grid_rowconfigure(i, weight=1)
        # for j in range(4):
        #     self.left_frame.grid_columnconfigure(j, weight=1)
        
        self.scrollable_course_frame.bind("<Configure>", self.resize_buttons)
                
        # for i in range(16):  # 16 행
        #     for j in range(4):  # 4 열
        #         # 각 칸에 Frame 생성
        #         cell_frame = ttk.Frame(left_frame, width=100, height=120)
        #         cell_frame.grid(row=i, column=j, padx=5, pady=5)
                
        #         # 이미지와 텍스트 레이블 추가
        #         image_num = i * 4 + j + 1
        #         image_name = f"course{image_num:03}.png"
        #         image_path = BASE_DIR / "static" / "images"
                
        #         try:
        #             image = Image.open(image_path)
        #             image = image.resize((100, 80), Image.ANTIALIAS)
        #             photo = ImageTk.PhotoImage(image)
        #             image_label = ttk.Label(cell_frame, image=photo)
        #             image_label.image = photo  # 참조 유지
        #             image_label.pack(side="top")

        #             # 텍스트 레이블
        #             text_label = ttk.Label(cell_frame, text=f"Course {image_num}")
        #             text_label.pack(side="bottom")
        #         except FileNotFoundError:
        #             print(f"Image not found: {image_path}")
        #             continue
        
    def resize_buttons(self, event):
        self.update_idletasks()
        new_width = self.scrollable_course_frame.winfo_width() // 4
        print(new_width)
        for button in self.course_buttons:
            button.config(
                width=new_width,
                height=self.image_height * new_width // self.image_width,
                compound="center",
            )
        
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
        
    def launch(self, t):
        self.course.delete(0, tk.END)
        self.course.insert(0, t)