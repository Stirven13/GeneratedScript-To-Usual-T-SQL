import tkinter
from tkinter import ttk


class StatusFrame(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master=master, highlightbackground="#a0a0a0", highlightthickness=1)
        self.initUI()

    def initUI(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("grey.Horizontal.TProgressbar", background='#555555')

        progress_bar = ttk.Progressbar(self, style='grey.Horizontal.TProgressbar', length=140)
        progress_bar.pack(side=tkinter.RIGHT)
        progress_bar["value"] = 50

        self.status_var = tkinter.StringVar(value="Загрузка")
        label_info = tkinter.Label(self, textvariable=self.status_var)
        label_info.pack(side=tkinter.RIGHT)


if __name__ == "__main__":
    root = tkinter.Tk()
    root.geometry("800x20")
    StatusFrame(root).pack(expand=True, fill=tkinter.BOTH, side=tkinter.BOTTOM)
    root.mainloop()
