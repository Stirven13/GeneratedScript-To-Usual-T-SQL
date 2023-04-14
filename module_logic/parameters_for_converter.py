import enum
import tkinter


class MethodWriteCreateTable(enum.Enum):
    unknown: int = -1
    default: int = 0
    alphabet: int = 0
    shuffle: int = 1


class MethodWriteInsert(enum.Enum):
    unknown: int = -1
    default: int = 0
    absolute_shuffle: int = 1
    shuffle_parts: int = 2
    smart_shuffe: int = 3


class MethodWriteConstraints(enum.Enum):
    unknown: int = -1
    default: int = 0
    absolute_shuffle: int = 1


class MethodWriteCommentaries(enum.Enum):
    unknown: int = -1
    default: int = 0
    smart_write: int = 0
    original_commentaries: int = 1


class ParametersForConverter:
    def __init__(self, master):
        self.write_use_db = tkinter.BooleanVar(master=master, value=True)

        self.write_create_table = tkinter.BooleanVar(master=master, value=True)
        self.method_write_create_table = tkinter.IntVar(master=master, value=MethodWriteCreateTable.default)

        self.write_insert = tkinter.BooleanVar(master=master, value=True)
        self.method_write_insert = tkinter.IntVar(master=master, value=MethodWriteInsert.default)

        self.write_constraints = tkinter.BooleanVar(master=master, value=True)
        self.method_write_constraints = tkinter.IntVar(master=master, value=MethodWriteConstraints.default)

        self.write_commentaries = tkinter.BooleanVar(master=master, value=False)
        self.method_write_commentaries = tkinter.IntVar(master=master, value=MethodWriteCommentaries.default)
