from doctest import master
import tkinter as tk
import tkinter.font as tkFont
from PIL import ImageTk, Image
from ctypes import windll

# import module for getting card information
import search_engine as search

from config import *


class App():
    def __init__(self) -> None:
        self.tk = tk.Tk()
        self.is_paused = True
        self.duel_mode = True
        self.configure_font()
        self.configure_control_area()
        self.configure_display_area()
        self.configure_window()

    def configure_font(self):
        if PREFERRED_FONT in tkFont.families():
            self.font = PREFERRED_FONT
        else:
            self.font = DEFAULT_FONT
    
    def configure_control_area(self):
        self.control_area = tk.Frame(
            master=self.tk, width=WINDOW_WIDTH, height=50)
        # button in control_area
        self.start_button = tk.Button(
            master=self.control_area,
            font=(self.font, BUTTON_FONT_SIZE),
            text="开始",
            width=10,
            height=1,
            bg=BLUE,
            fg="white",
            command=self.pause_unpause,
        )
        self.mode_button = tk.Button(
            master=self.control_area,
            font=(self.font, BUTTON_FONT_SIZE),
            text="切换至决斗",
            width=10,
            height=1,
            bg=BLUE,
            fg="white",
            command=self.switch_mode,
        )
        self.exit_button = tk.Button(
            master=self.control_area,
            font=(self.font, BUTTON_FONT_SIZE),
            text="退出",
            width=10,
            height=1,
            bg=RED,
            fg="white",
            command=self.exit,
        )
        self.control_area.pack(fill=tk.BOTH, expand=False)
        self.start_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.mode_button.pack(side=tk.RIGHT, padx=10, pady=10)
        self.exit_button.place(relx=.5, rely=.5,anchor=tk.CENTER)

    def configure_display_area(self):
        self.display_area = tk.Frame(
            master=self.tk, width=WINDOW_WIDTH, height=200)
        # contents in display_area
        self.card_pic = tk.Label(
            master=self.display_area,
            image=None,
        )
        self.card_name = tk.Label(
            master=self.display_area,
            font=(self.font, CARD_NAME_SIZE, 'bold'),
            text="",
            fg=BLUE,
        )
        self.card_desc = tk.Message(
            master=self.display_area,
            font=(self.font, CARD_DESC_SIZE),
            text="",
            justify=tk.LEFT,
            # width in piels, -20 to leave room for special characters
            width=WINDOW_WIDTH - 20
        )
        self.display_area.pack(fill=tk.BOTH, expand=True)
        self.card_pic.pack()
        self.card_name.pack()
        self.card_desc.pack()

    def configure_window(self):
        self.tk.minsize(200, 200)
        # manually resizing th window will cause th window to stop auto resizing, therefore disabled
        self.tk.resizable(False, False)
        self.tk.overrideredirect(True)
        self.tk.attributes("-topmost", True)
        self.tk.geometry(f"+{START_POS_X}+{START_POS_Y}")
        self.configure_dragger(self.control_area)
        self.configure_dragger(self.display_area)
        self.configure_dragger(self.card_pic)
        self.configure_dragger(self.card_name)
        self.configure_dragger(self.card_desc)

    def update_display_area(self, last_card):
        current_card = search.get_card_No()
        if current_card and current_card != last_card:
            last_card = current_card
            # 83764718 and 83764719 are different Shishasoses
            card_number = "83764718" if current_card == "83764719" else current_card
            self.load_card(card_number, True)
        self.tk.after(UPDATE_INTERVAL,
                      lambda: self.update_display_area(last_card))
    
    def load_card(self, card_number, show_card_desc):
        try:
            with Image.open("pics/" + card_number + ".jpg") as file:
                img = ImageTk.PhotoImage(file)
                self.card_pic.configure(image=img)
                self.card_pic.image = img
        except FileNotFoundError:
            pass

        if show_card_desc:
            self.card_name["text"] = search.get_card_name()
            self.card_desc["text"] = search.get_card_desc()


    def pause_unpause(self):
        if self.is_paused:
            search.unpause()
            self.start_button.configure(text="暂停")
            self.is_paused = False
        else:
            search.pause()
            self.start_button.configure(text="继续")
            self.is_paused = True

    def switch_mode(self):
        if self.duel_mode:
            search.switch_mode()
            self.mode_button.configure(text="切换至组卡")
            self.duel_mode = False
        else:
            search.switch_mode()
            self.mode_button.configure(text="切换至决斗")
            self.duel_mode = True

    def configure_dragger(self, widget):
        widget.bind("<ButtonPress-1>", self.start_move)
        widget.bind("<ButtonRelease-1>", self.stop_move)
        widget.bind("<B1-Motion>", self.do_move)

    def start_move(self, event):
        self.tk.x = event.x
        self.tk.y = event.y

    def stop_move(self, event):
        self.tk.x = None
        self.tk.y = None

    def do_move(self, event):
        deltax = event.x - self.tk.x
        deltay = event.y - self.tk.y
        x = self.tk.winfo_x() + deltax
        y = self.tk.winfo_y() + deltay
        self.tk.geometry(f"+{x}+{y}")

    def start(self):
        search.start()
        self.tk.after(UPDATE_INTERVAL, self.update_display_area(DEFAULT_PIC))
        self.load_card(DEFAULT_PIC, False)
        self.tk.mainloop()

    def exit(self):
        self.tk.destroy()
        search.kill()


def main():
    # Support high DPI displays
    windll.shcore.SetProcessDpiAwareness(1)
    app = App()
    app.start()

if __name__ == "__main__":
    main()
