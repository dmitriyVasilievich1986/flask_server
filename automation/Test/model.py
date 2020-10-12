from ..database import DataBase, Model, Column, STRING, INTEGER, Relationship

import json


class ModuleTest(Model):
    db = DataBase(
        "module_test",
        Column("module_id", INTEGER),
        Column("test_id", INTEGER),
    )

    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(**kwargs)


class Test(Model):
    db = DataBase(
        "test",
        Relationship("")
    )

    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(**kwargs)
