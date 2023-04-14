import tkinter


class SeparatorFrame(tkinter.Frame):
    def __init__(self, master, resize_columns):
        super().__init__(master=master, width=5, background="#c8c8c8")
        self.resize_columns = resize_columns
        self.bind("<Enter>", lambda event: self.config(cursor="sb_h_double_arrow"))
        self.bind("<B1-Motion>", self.resize_columns)
        self.pack_propagate(False)
