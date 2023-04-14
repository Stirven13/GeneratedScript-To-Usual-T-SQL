import re
import copy


class ConverterSQL:
    def __init__(self, input_script: str | None = None):
        self.set_script(input_script=input_script)
        self.db_info = DataBaseInfo()

    def set_script(self, input_script):
        self.original_script = input_script
        self.input_script = copy.copy(input_script)

    def convert(self):
        self.db_info = DataBaseInfo()
        self.delete_commentaries()
        self.find_use_db_name()
        self.find_tables()
        self.find_constraint()
        self.find_insert_data()
        return self.build_usual_sql()

    def build_usual_sql(self):
        sql_output = ""
        if self.db_info.name_db is not None:
            sql_output += f"USE {self.db_info.name_db}\n\n\n"

        sql_output += "\n\n".join(["\n\n".join(code for name, code in self.db_info.tables.items()),
                                   "\n\n".join(data_field for data_field in self.db_info.insert_data),
                                   "\n\n".join(constraint for constraint in self.db_info.constraints)])
        return sql_output

    def delete_commentaries(self):
        if self.db_info.count_commentaries == 0:
            return
        self.input_script, self.db_info.count_commentaries = re.subn(ReFormats.find_comment, "", self.input_script)
        self.input_script = "\n".join(
            [line.strip() for line in self.input_script.splitlines() if len(line.strip()) != 0])

    def find_use_db_name(self):
        find_use_db_name_search_re = re.search(ReFormats.find_use_db_name, self.input_script)
        if find_use_db_name_search_re:
            self.db_info.name_db = find_use_db_name_search_re[3]

    def find_tables(self):
        for part in self.input_script.split("GO"):
            part = part.strip()
            try_detect_table = re.search(ReFormats.find_create_table, part)
            if not try_detect_table:
                continue
            sql_create_table = ""
            create_table_re_search = re.search(ReFormats.find_create_table, part).groups()
            if " " in create_table_re_search[2]:
                sql_create_table += "CREATE TABLE [" + create_table_re_search[2] + "] (\n"
            else:
                sql_create_table += "CREATE TABLE " + create_table_re_search[2] + " (\n"

            primary_key_index = part.split("PRIMARY KEY")[0].count("\n")
            sql_input_splited_by_line = part.split("\n")
            for field in sql_input_splited_by_line[1:primary_key_index]:
                sql_create_table += self.field_of_create_table_conversion(field) + "\n"

            primary_key_line = self.primary_key_of_create_table_reformat(sql_input_splited_by_line[primary_key_index:])
            if primary_key_line == "":
                self.db_info.tables[create_table_re_search[2]] = sql_create_table + "\n)"
            else:
                self.db_info.tables[create_table_re_search[2]] = sql_create_table + "  " + primary_key_line + "\n)"

    def field_of_create_table_conversion(self, field):
        field = field.strip()
        splited_field = field.split("] [")
        if field.index(" ") < field.index("]"):
            changed_field = splited_field[0] + "] " + splited_field[1].replace("]", "", 1)
        else:
            changed_field = splited_field[0][1:] + " " + splited_field[1].replace("]", "", 1)
        if "NOT NULL" not in field:
            changed_field = changed_field.replace(" NULL", "")
        return "  " + changed_field

    def primary_key_of_create_table_reformat(self, sql_primary_key_part):
        all_primary_keys = []
        for line in sql_primary_key_part:
            founded = re.search(ReFormats.find_primary_key_field, line)
            if not founded:
                continue
            if " " in founded.groups()[1]:
                all_primary_keys.append("[" + founded.groups()[1] + "]")
            else:
                all_primary_keys.append(founded.groups()[1])

        if len(all_primary_keys) == 0:
            return ""
        return "PRIMARY KEY (" + ", ".join(all_primary_keys) + ")"

    def find_constraint(self):
        for part in self.input_script.split("GO"):
            part = part.strip().replace("[dbo].", "").replace("  ", " ")
            try_detect_constraint = re.search(ReFormats.find_add_constraint, part)
            if not try_detect_constraint:
                continue
            part = ReFormats.find_name_without_space.sub(lambda match: match.group().replace('[', '').replace(']', ''),
                                                         part)
            self.db_info.constraints.append(part)

    def find_insert_data(self):
        for part in self.input_script.split("GO"):
            part = part.strip().replace("[dbo].", "")
            try_detect_insert_data = re.search(ReFormats.find_insert_into, part)
            if not try_detect_insert_data:
                continue
            part = ReFormats.find_name_without_space.sub(lambda match: match.group().replace('[', '').replace(']', ''),
                                                         part)
            self.db_info.insert_data.append(part)


class DataBaseInfo:
    name_db: str | None = None
    count_create_table = 0
    count_references = 0
    count_commentaries = 0
    count_go = 0
    tables = {}
    constraints = []
    insert_data = []


class ReFormats:
    find_use_db_name = re.compile("(USE )(\[)(.*?)(\])")
    find_comment = re.compile("/\*{6}[\s\S]*?\*/")
    find_create_table = re.compile("(CREATE TABLE)( \[dbo\].\[)(.*?)(\])")
    find_primary_key_field = re.compile("(\[)(.*?)(\] ASC)")
    find_add_constraint = re.compile("(ALTER(\s*)TABLE)(.*?)(ADD(\s*)CONSTRAINT)")
    find_name_without_space = re.compile("\[[^\s]+\]")
    find_insert_into = re.compile("(INSERT)(.*?)(VALUES)")


if __name__ == "__main__":
    with open(r"../data/temp_sql_script2.sql", "r", encoding="utf-8") as file:
        sql_script = file.read()
    converter = ConverterSQL(sql_script)
    print(converter.convert())
