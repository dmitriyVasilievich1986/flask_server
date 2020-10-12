STRING = "TEXT"
INTEGER = "INTEGER"


class Column(object):
    def __init__(self, name, type_, value=None, primary_key=False, nullable=True, unique=False):
        self.name = name
        self.value = value
        self.type_ = type_
        self.primary_key = primary_key
        self.nullable = nullable
        self.unique = unique
        if type_ == STRING:
            self._type = str
            self.default = ""
        elif type_ == INTEGER:
            self._type = int
            self.default = 0

    def __str__(self):
        return "{} {}{}{}{}".format(
            self.name,
            self.type_,
            " PRIMARY KEY" if self.primary_key else "",
            "" if self.nullable else " NOT NULL",
            " UNIQUE" if self.unique else ""
        )


class Relationship(object):
    def __init__(self, name, reference_table_name, relate_class):
        self.name = name
        self.relate_class = relate_class
        self.reference_table_name = reference_table_name

    def __str__(self):
        return "{} INTEGER, FOREIGN KEY ({}) REFERENCES {}(id)".format(
            self.name,
            self.name,
            self.reference_table_name
        )


class BackRef(object):
    def __init__(self, backref_class):
        self.backref_class = backref_class
