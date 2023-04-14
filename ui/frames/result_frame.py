import tkinter

try:
    import pyperclip
except ModuleNotFoundError:
    pass


class OutputText(tkinter.LabelFrame):
    def __init__(self, master, output_text_var: tkinter.StringVar | None = None):
        super().__init__(master=master, text="Конвертированный запрос")
        if output_text_var is None:
            output_text_var = tkinter.StringVar(master)
        self.output_text_var = output_text_var
        self.output_text_var.get = self.getText
        self.output_text_var.set = self.setText
        self.initUI()

    def initUI(self):
        """
        Тут можно сделать настройку для wrap у text_bot - WORD или CHAR или NONE

        А ещё можно будет менять настройку шрифта, тип размер и всякое такой. Однако нужно будет тогда добавить и конфиг
        мб его попробовать как-то переделать, чтобы сделать сохранение в exe файла.
        """
        self.pack(fill=tkinter.BOTH, expand=tkinter.YES)

        self.text_box = tkinter.Text(self, font=("consolas", 10), undo=True, wrap=tkinter.WORD)  # WORD or CHAR
        self.text_box.pack(expand=True, fill=tkinter.BOTH)

        vertical_scrollbar = tkinter.Scrollbar(self.text_box, orient=tkinter.VERTICAL, command=self.text_box.yview)
        vertical_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.text_box["yscrollcommand"] = vertical_scrollbar.set

        if self.text_box["wrap"] == tkinter.NONE:
            horizontal_scrollbar = tkinter.Scrollbar(self.text_box, orient=tkinter.HORIZONTAL,
                                                     command=self.text_box.xview)
            horizontal_scrollbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
            self.text_box["xscrollcommand"] = horizontal_scrollbar.set

    def clearText(self):
        self.text_box.delete(1.0, tkinter.END)

    def getText(self):
        return self.text_box.get(1.0, tkinter.END)

    def setText(self, value: str):
        self.clearText()
        self.text_box.insert(1.0, value)


class OutputButtonConverterFrame(tkinter.Frame):
    def __init__(self, master, output_text_var: tkinter.StringVar | None = None):
        super().__init__(master=master)
        if output_text_var is None:
            self.input_text_var = tkinter.StringVar(master)
        self.input_text_var = output_text_var
        self.initUI()

    def initUI(self):
        button_copy_in_clipboard = tkinter.Button(master=self, text="Копировать",
                                                  command=self.copy_in_clipboard_input_text_var)
        button_copy_in_clipboard.pack(side=tkinter.RIGHT)

    def copy_in_clipboard_input_text_var(self):
        pyperclip.copy(self.input_text_var.get())


class OutputFrame(tkinter.Frame):
    def __init__(self, master, output_text_var: tkinter.StringVar | None = None):
        super().__init__(master=master)
        if output_text_var is None:
            self.output_text_var = tkinter.StringVar(master)
        self.output_text_var = output_text_var
        self.initUI()

    def initUI(self):
        OutputText(self, output_text_var=self.output_text_var).pack(expand=True, fill=tkinter.BOTH)
        if "pyperclip" in globals():
            OutputButtonConverterFrame(self, output_text_var=self.output_text_var).pack(fill=tkinter.BOTH)
