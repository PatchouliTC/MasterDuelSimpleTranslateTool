import tkinter as tk
from PIL import ImageTk, Image

from threading import Thread
import master_duel_auto_scan_version as mda

# front for the card description only
FRONT_SIZE = 15
FRONT = '微软雅黑'

# default card pic to show when there's no match
# ideally should be the card back
DEFAULT_PIC = 10000


class App():
    def __init__(self) -> None:
        self.tk = tk.Tk()
        self.tk.title("ygoMD translater")
        self.tk.minsize(200, 200)
        self.frame_control = tk.Frame(master=self.tk, width=400, height=50)
        self.frame_show = tk.Frame(master=self.tk, width=400, height=200)

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

        # no need to show name
        # self.card_name = tk.Label(
        #     master=self.frame_show,
        #     font=("Courier", 33),
        #     text=""
        # )

        self.card_desc = tk.Message(
            master=self.frame_show,
            font=(FRONT, FRONT_SIZE),
            text="",
            justify=tk.LEFT,
            # width in piels, the original width of the card pics is 400
            # this width is slightly smaller to leave room for special characters
            width=380
        )

        self.frame_control.pack(fill=tk.BOTH, expand=False)
        self.button_Start.pack(side=tk.LEFT)
        self.button_Mode.pack(side=tk.RIGHT)
        self.frame_show.pack(fill=tk.BOTH, expand=True)

        # no need to show name
        # self.card_name.pack()
        try:
            with Image.open('pics/10000.jpg') as file:
                img = ImageTk.PhotoImage(file)
                self.card_pic = tk.Label(
                    master=self.frame_show,
                    image=img
                )
                self.card_pic.image = img
                self.card_pic.pack()
        except FileNotFoundError:
            pass

        self.card_desc.pack()

    def update_frame_show(self, last_card):

        if mda.g_card_show and mda.g_card_show["card"] != last_card:
            last_card = mda.g_card_show["card"]

            # no need to show name
            # self.card_name["text"] = mda.g_card_show["name"]
            self.card_desc["text"] = mda.g_card_show["desc"]
            try:
                with Image.open('pics/' + mda.g_card_show['card'] + '.jpg') as file:
                    img = ImageTk.PhotoImage(file)
                    self.card_pic.configure(image=img)
                    self.card_pic.image = img
            except FileNotFoundError:
                pass

        self.tk.after(100, lambda: self.update_frame_show(last_card))

# kill the searching thread and the gui when exit


def on_close(app):
    mda.status_change(False, False, True)
    app.tk.destroy()


def main():
    app = App()

    scan_card = Thread(target=mda.main)
    scan_card.start()

    app.tk.protocol("WM_DELETE_WINDOW", lambda: on_close(app))

    app.tk.after(1000, app.update_frame_show(DEFAULT_PIC))
    # put window on top
    app.tk.attributes('-topmost', True)
    app.tk.mainloop()


if __name__ == '__main__':
    main()
