import tkinter as tk
from PIL import ImageTk, Image

from threading import Thread
import master_duel_auto_scan_version as mda

# front for the texts
FRONT_SIZE = 15
FRONT = '微软雅黑'

# default card pic to show when there's no match
# ideally should be the card back
DEFAULT_PIC = "10000"

# the width of the card pic files is 400
WINDOW_WIDTH = 400

# interval for updating info in gui, in ms, independent from searching
UPDATE_INTERVAL = 50


class App():
    def __init__(self) -> None:
        self.tk = tk.Tk()
        self.tk.title("ygoMD translater")
        self.tk.minsize(200, 200)
        # manually resizing th window will cause th window to stop auto resizing, therefore disabled
        self.tk.resizable(False, False)
        self.frame_control = tk.Frame(
            master=self.tk, width=WINDOW_WIDTH, height=50)
        self.frame_show = tk.Frame(
            master=self.tk, width=WINDOW_WIDTH, height=200)

        # button in frame_control
        self.button_Start = tk.Button(
            master=self.frame_control,
            text="暂停",
            width=10,
            height=2,
            bg="grey",
            fg="blue",
            command=lambda: mda.status_change(False, True, False)
        )

        self.button_Mode = tk.Button(
            master=self.frame_control,
            text="组卡/决斗",
            width=10,
            height=2,
            bg="grey",
            fg="blue",
            command=lambda: mda.status_change(True, False, False)
        )

        # contents in frame_show
        self.card_desc = tk.Message(
            master=self.frame_show,
            font=(FRONT, FRONT_SIZE),
            text="",
            justify=tk.LEFT,
            # width in piels, -20 to leave room for special characters
            width=WINDOW_WIDTH - 20
        )

        self.frame_control.pack(fill=tk.BOTH, expand=False)
        self.button_Start.pack(side=tk.LEFT)
        self.button_Mode.pack(side=tk.RIGHT)
        self.frame_show.pack(fill=tk.BOTH, expand=True)

        try:
            with Image.open("pics/" + DEFAULT_PIC + ".jpg") as file:
                img = ImageTk.PhotoImage(file)
                self.card_pic = tk.Label(
                    master=self.frame_show,
                    image=img
                )
                self.card_pic.image = img
                self.card_pic.pack()
        except FileNotFoundError:
            # if fail to load pic, show the name instead
            self.card_name = tk.Label(
                master=self.frame_show,
                font=(FRONT, FRONT_SIZE),
                text=""
            )
            self.card_name.pack()

        self.card_desc.pack()

    def update_frame_show(self, last_card):

        if mda.g_card_show and mda.g_card_show["card"] != last_card:
            last_card = mda.g_card_show["card"]

            try:
                # 83764718 and 83764719 are different Shishasoses
                card_No = "83764718" if mda.g_card_show["card"] == "83764719" else mda.g_card_show["card"]
                with Image.open("pics/" + card_No + ".jpg") as file:
                    img = ImageTk.PhotoImage(file)
                    self.card_pic.configure(image=img)
                    self.card_pic.image = img
            except FileNotFoundError:
                # if fail to load pic, show the name instead
                self.card_name["text"] = mda.g_card_show["name"]

            self.card_desc["text"] = mda.g_card_show["desc"]

        self.tk.after(UPDATE_INTERVAL,
                      lambda: self.update_frame_show(last_card))

# kill the searching thread and the gui when exit


def on_close(app):
    mda.status_change(False, False, True)
    app.tk.destroy()


def main():
    app = App()

    scan_card = Thread(target=mda.main)
    scan_card.start()

    app.tk.protocol("WM_DELETE_WINDOW", lambda: on_close(app))

    app.tk.after(UPDATE_INTERVAL, app.update_frame_show(DEFAULT_PIC))
    # put window on top
    app.tk.attributes("-topmost", True)
    app.tk.mainloop()


if __name__ == "__main__":
    main()
