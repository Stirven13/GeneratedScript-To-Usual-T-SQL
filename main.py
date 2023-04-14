import tkinter
from module_logic import ConverterSQL, ParametersForConverter
from ui.frames import InputFrame, SeparatorFrame, OutputFrame, StatusFrame


class Application(tkinter.Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("GeneratedScript To Usual SQL-T")
        self.minsize(width=200, height=300)
        self.geometry("800x600")
        self.iconbitmap("data/icon.ico")
        self.resizable(True, True)
        self.background_color = "#f0f0f0"
        self.pixelVirtual = tkinter.PhotoImage(width=1, height=1)

        self.converter = ConverterSQL()
        self.parameters_for_convert = ParametersForConverter(self)
        self.input_text_var = tkinter.StringVar(self)
        self.output_text_var = tkinter.StringVar(self)
        self.initUI()

    def initUI(self):
        # self.status_frame = StatusFrame(self)
        # self.status_frame.pack(side=tkinter.BOTTOM, anchor=tkinter.SE, fill=tkinter.BOTH)
        self.input_frame = InputFrame(self, converter=self.converter, input_text_var=self.input_text_var,
                                      parameters_for_convert=self.parameters_for_convert, do_convert=self.do_convert, )
        self.input_frame.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH)
        self.input_frame.pack_propagate(False)

        self.separator = SeparatorFrame(self, self.resize_columns)
        self.separator.pack(side=tkinter.LEFT, fill=tkinter.BOTH)

        self.output_frame = OutputFrame(self, output_text_var=self.output_text_var)
        self.output_frame.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH)
        self.output_frame.pack_propagate(False)

        self.bind('<Configure>', self.change_configure)

    def resize_columns(self, event: tkinter.Event):
        change_ = event.x_root - self.separator.winfo_rootx()

        self.input_frame.config(width=self.input_frame.winfo_width() + change_)
        self.output_frame.config(width=self.output_frame.winfo_width() - change_)

    def change_configure(self, event: tkinter.Event):
        persent_new_size = (self.winfo_width() - self.separator.winfo_width()) / (
                self.input_frame.winfo_width() + self.output_frame.winfo_width())

        self.input_frame.config(width=self.input_frame.winfo_width() * persent_new_size)
        self.output_frame.config(width=self.output_frame.winfo_width() * persent_new_size)

    def do_convert(self):
        self.converter.set_script(self.input_text_var.get())
        sql_script = self.converter.convert()
        self.output_text_var.set(value=sql_script)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
