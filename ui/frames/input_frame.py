import tkinter
from tkinter import ttk

from module_logic import ParametersForConverter, ConverterSQL


class InputText(tkinter.LabelFrame):
    def __init__(self, master, input_text_var: tkinter.StringVar | None = None):
        super().__init__(master=master, text="Ввод SQL запроса")
        if input_text_var is None:
            self.input_text_var = tkinter.StringVar(master)
        else:
            self.input_text_var = input_text_var
        self.input_text_var.get = self.getText
        self.input_text_var.set = self.setText

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
        vertical_scrollbar.bind("<Enter>", lambda event: self.config(cursor="arrow"))

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


class InputSetting(tkinter.LabelFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.parameters_for_convert = ParametersForConverter(master=master)
        self.initUI()

    def initUI(self):
        super().__init__(master=self.master, text="Параметры конвертации")
        self.pack(fill=tkinter.BOTH)
        frame_checkboxes = tkinter.Frame(self)
        checkbox_use_db = tkinter.Checkbutton(frame_checkboxes,
                                              variable=self.parameters_for_convert.write_use_db,
                                              text="Добавить: USE DatabaseName")
        checkbox_use_db.pack(anchor=tkinter.NW)
        tkinter.Checkbutton(frame_checkboxes,
                            variable=self.parameters_for_convert.write_create_table,
                            text="Добавить: CREATE TABLE").pack(anchor=tkinter.NW)
        tkinter.Checkbutton(frame_checkboxes,
                            variable=self.parameters_for_convert.write_insert,
                            text="Добавить: INSERT VALUE").pack(anchor=tkinter.NW)
        tkinter.Checkbutton(frame_checkboxes,
                            variable=self.parameters_for_convert.write_constraints,
                            text="Добавить: ADD CONSTRAINT").pack(anchor=tkinter.NW)
        tkinter.Checkbutton(frame_checkboxes,
                            variable=self.parameters_for_convert.write_commentaries,
                            text="Добавить: комментарии").pack(anchor=tkinter.NW)
        frame_checkboxes.pack(side=tkinter.LEFT)


class InputButtonConverterFrame(tkinter.Frame):
    def __init__(self, master, input_text_var: tkinter.StringVar | None = None, do_convert=None):
        super().__init__(master=master)
        if input_text_var is None:
            self.input_text_var = tkinter.StringVar(master)
        else:
            self.input_text_var = input_text_var
        self.do_convert = do_convert
        self.initUI()

    def initUI(self):
        button_convert = tkinter.Button(master=self, text="Конвертировать", command=self.do_convert)
        button_convert.pack(side=tkinter.RIGHT)

        button_clear = tkinter.Button(master=self, text="Очистить", command=lambda: self.input_text_var.set(""))
        button_clear.pack(side=tkinter.RIGHT)


class InputFrame(tkinter.Frame):
    def __init__(self, master, converter=ConverterSQL(), parameters_for_convert: ParametersForConverter | None = None,
                 do_convert=None, input_text_var: tkinter.StringVar | None = None):
        super().__init__(master=master)
        self.converter = converter

        if parameters_for_convert is None:
            parameters_for_convert = ParametersForConverter(master=master)
        self.parameters_for_convert = parameters_for_convert

        self.do_convert = do_convert

        if input_text_var is None:
            input_text_var = tkinter.StringVar(master)
        self.input_text_var = input_text_var

        self.initUI()

    def initUI(self):
        InputText(self, input_text_var=self.input_text_var).pack(expand=True, fill=tkinter.BOTH)
        InputSetting(self).pack(fill=tkinter.BOTH)
        InputButtonConverterFrame(self, input_text_var=self.input_text_var, do_convert=self.do_convert).pack(
            fill=tkinter.BOTH)


if __name__ == "__main__":
    root = tkinter.Tk()
    root.geometry("400x600")
    InputFrame(root).pack(expand=True, fill=tkinter.BOTH)
    root.mainloop()
