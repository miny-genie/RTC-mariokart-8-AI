import re
from queue import Empty

from pandastable import Table
import tkinter as tk
from tkinter import PhotoImage, ttk
import webbrowser

from playground.config import Config
from playground.constants import BASE_DIR
from playground.utils import is_windows


class ScrolledText(ttk.Frame):
    def __init__(self, parent, height, state, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.text = tk.Text(self, wrap="none", height=height, state=state)
        vsb = ttk.Scrollbar(self, command=self.text.yview, orient="vertical")
        self.text.configure(yscrollcommand=vsb.set)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0,weight=1)
        
        # Keycode for ScrolledText UI drawing
        vsb.grid(row=0, column=1, sticky="ns")
        self.text.grid(row=0, column=0, sticky="nsew")


# Adapted from https://beenje.github.io/blog/posts/logging-to-a-tkinter-scrolledtext-widget/
class ConsoleWindow(ttk.Frame):
    def __init__(self, queue_handler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Create a ScrollText widget
        self.scrolled_text = ScrolledText(self, height=5, state="disabled")
        self.scrolled_text.pack(expand=True, fill="both")
        self.scrolled_text.text.configure(font="TkFixedFont")
        self.scrolled_text.text.tag_config("INFO", foreground="green")
        self.scrolled_text.text.tag_config("DEBUG", foreground="gray")
        self.scrolled_text.text.tag_config("WARNING", foreground="orange")
        self.scrolled_text.text.tag_config("ERROR", foreground="red")
        self.scrolled_text.text.tag_config("CRITICAL", foreground="red", underline=1)
        
        # Create a logging handler using a queue
        self.queue_handler = queue_handler
        
        # Start polling messages using a queue
        self.after(100, self.poll_log_queue)
        
    def display(self, record):
        msg = self.queue_handler.format(record)
        self.scrolled_text.text.configure(state="normal")
        self.scrolled_text.text.insert(tk.END, msg + "\n", record.levelname)
        self.scrolled_text.text.configure(state="disabled")
        self.scrolled_text.text.yview(tk.END)
    
    def poll_log_queue(self):
        while True:
            try:
                record = self.queue_handler.log_queue.get(block=False)
            except Empty:
                break
            else:
                self.display(record)
        self.after(100, self.poll_log_queue)
        
    def close(self):
        pass


class ScrollableMixin:
    def on_theme_change(self, _event):
        background = self.style.lookup("TFrame", "background")
        self.canvas.configure(background=background)
        self.winfo_toplevel().configure(background=background)
    
    def _configure_interior(self, _event):
        size = (
            self.scrollable_frame.winfo_reqwidth(),
            self.scrollable_frame.winfo_reqheight(),
        )
        self.canvas.config(scrollregion="0 0 %s %s" % size)
        
        if self.scrollable_frame.winfo_reqwidth() != self.winfo_width():
            # update the canvas's width to fit the inner frame
            self.canvas.config(width=self.scrollable_frame.winfo_reqwidth())
    
    def _configure_canvas(self, _event):
        if self.scrollable_frame.winfo_reqwidth() != self.winfo_width():
            # update the inner frame's width to fill the canvas
            self.canvas.itemconfigure(self.interior_id, width=self.winfo_width())
    
    def _on_mousewheel(self, event):
        scroll_dir = None
        if event.num == 5 or event.delta == -120:
            scroll_dir = 1
        elif event.num == 4 or event.delta == 120:
            scroll_dir = -1
            
        if scroll_dir is None:
            return
        
        # If the scrollbar is max size don't bother scrolling
        if self.vscrollbar.get() == (0.0, 1.0):
            return
        
        self.canvas.yview_scroll(scroll_dir, "units")
    
    def _bind_to_mousewheel(self, _event):
        if is_windows():
            self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        else:
            self.canvas.bind_all("<Button-4>", self._on_mousewheel)
            self.canvas.bind_all("<Button-5>", self._on_mousewheel)
    
    def _unbind_from_mousewheel(self, _event):
        if is_windows():
            self.canvas.unbind_all("<MouseWheel>")
        else:
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")


class ScrollableFrameLegacy(ScrollableMixin, ttk.LabelFrame):
    def __init__(self, parent, *args, **kw):
        ttk.LabelFrame.__init__(self, parent, *args, **kw)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        # Adapted from https://gist.github.com/JackTheEngineer/81df334f3dcff09fd19e4169dd560c59
        # create a canvas object and a vertical scrollbar for scrolling it.
        self.vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.vscrollbar.grid(row=0, column=1, sticky="nse")
        
        self.style = ttk.Style()
        background = self.style.lookup("TFrame", "background")
        
        self.canvas = tk.Canvas(self, bg=background, yscrollcommand=self.vscrollbar.set)
        self.bind_all("<<ThemeChange>>", self.on_theme_change)
        self.canvas.grid(row=0, column=0, sticky="nswe")
        self.vscrollbar.config(command=self.canvas.yview)
        
        # reset the view.
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
        
        # create a frame inside the canvas which will be scrolled with it.
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.interior_id = self.canvas.create_window(
            0, 0, window=self.scrollable_frame, anchor=tk.NW,
        )
        
        self.scrollable_frame.bind("<Configure>", self._configure_interior)
        self.canvas.bind("<Configure>", self._configure_canvas)
        self.canvas.bind("<Enter>", self._bind_to_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_from_mousewheel)


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
        self.widget.bind("<Motion>", self.on_motion)
        
        self.tooltip = None
        self.label = None
        
    def set_geometry(self, event):
        root = self.widget.winfo_toplevel()
        screen_width = root.winfo_screenwidth()
        (width, _, _, _) = list(map(int, re.split(r"[x+]", self.tooltip.geometry())))
        
        x_coord = event.x_root + 15
        if event.x_root > screen_width * 0.70:
            x_coord = event.x_root - width - 15
            
        y_coord = event.y_root + 10
        
        self.tooltip.geometry(f"+{x_coord}+{y_coord}")
        
    def on_enter(self, event):
        self.tooltip = tk.Toplevel()
        self.tooltip.overrideredirect(True)
        self.set_geometry(event)
    
    def on_leave(self, _event):
        self.tooltip.destroy()
    
    def on_motion(self, event):
        self.set_geometry(event)


class Tab(ttk.Frame):
    """Base class that all tabs should inherit from."""
    
    show_console = True
    save_needed = False
    
    def on_load(self):
        """Called whenever the tab is loaded."""


class Entry(ttk.Entry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind("<Control-a>", self.select_all)
        
    def select_all(self, event):
        event.widget.select_range(0, "end")
        event.widget.icursor("end")
        return "break"


class DebounceEntry(Entry):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.bind("<Key>", self._on_key)
        
        self._on_key_func = None
        self._after_id = None
        self._debounce_ms = 200
        
    def _on_key(self, event=None):
        if self._on_key_func is None:
            return
        
        if self._after_id is not None:
            self.after_cancel(self._after_id)
        self._after_id = self.after(self._debounce_ms, self._on_key_func, event)
    
    def bind_on_key(self, func, debounce_ms=None):
        self._on_key_func = func
        if debounce_ms is not None:
            self._debounce_ms = debounce_ms


class CustomTable(Table):
    def __init__(self, parent, dataframe, *args, **kwargs):
        super().__init__(parent, dataframe=dataframe, editable=False, *args, **kwargs)
        self.font = "Malgun Gothic"
        self.fontsize = "10"
        self.setFont()
        self.setTheme("default")    # dark, bold