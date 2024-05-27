import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from playground.config import Config, MIN_WIDTH, MIN_HEIGHT
from playground.constants import BASE_DIR
from playground.ui.widgets import ScrollableFrameLegacy, Tab


class ExtractTab(Tab):
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
        
        # Course Frame
        self.scrollable_course_frame = ScrollableFrameLegacy(self, text="Course")
        self.scrollable_course_frame.grid(row=0, column=0, sticky="nsew")
        self.course_frame = ttk.Frame(
            self.scrollable_course_frame.scrollable_frame
        )
        self.course_frame.grid(row=0, column=0, sticky="nsew")
        
        # Frame Sepatator
        sep = ttk.Separator(self, orient=tk.VERTICAL)
        sep.grid(row=0, column=1, padx=10, sticky="ns")
        
        # Unsafe Playground Frame
        self.right_frame = ttk.Frame(self)
        self.right_frame.grid(row=0, column=2, sticky="nsew")
        
        # Play Button
        self.button_play = ttk.Button(
            self.right_frame, text="불안전한 놀이터!",
        )
        self.button_play.grid(row=0, column=0, pady=5, padx=5, sticky="swe")
        
        # Course Info
        # self.course_label = ttk.Label(setext="맵 이름: ")
        # self.course = ttk.Entry()
        
        # Configure
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, minsize=450)
        
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
        
    def update_buttons(self):
        for i, button in enumerate(self.course_buttons):
            image = self.load_image(i + 1, self.image_width, self.image_height)
            button.config(image=image, width=self.image_width, height=self.image_height)
            button.image = image  # 참조 유지
        
    def create_resized_image(image_path, target_width, target_height):
        image = Image.open(image_path)
        resized_image = image.resize((target_width, target_height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(resized_image)
    
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