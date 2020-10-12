from ..database import Column, STRING, INTEGER, Relationship, DataBase, Model
import json


class Module(Model):
    db = DataBase(
        "module",
        Column("name", STRING, unique=True, nullable=False),
        Column("text", STRING, nullable=False),
        Column("description", STRING),
        Column("sending_data", STRING),
    )

    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(**kwargs)
