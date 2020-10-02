from ..application.database import db
from ..modules import Module

import json

module_test = db.Table(
    "module_test",
    db.Column("module_id", db.Integer, db.ForeignKey("module.id"), primary_key=True),
    db.Column("test_id", db.Integer, db.ForeignKey("test.id"), primary_key=True)
)


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    text = db.Column(db.String(20), nullable=False)
    command = db.Column(db.String(20), nullable=False)
    tag = db.Column(db.String(20))
    description = db.Column(db.String(200))

    start_position = db.Column(db.Integer, default=0)
    count = db.Column(db.Integer, default=0)
    min_value = db.Column(db.Integer, default=0)
    max_value = db.Column(db.Integer, default=0)
    none_value = db.Column(db.Integer, default=0)

    modules = db.relationship(
        'Module',
        secondary=module_test,
        lazy='subquery',
        backref=db.backref('tests', lazy=True)
    )

    def __init__(
        self,
        name=None,
        text=None,
        command=None,
        count=None,
        min_value=None,
        max_value=None,
        none_value=None,
        start_position=None,
        modules=None,
        tag=None,
        description=None,
        *args,
        **kwargs
    ):
        self.name = name or self.name
        self.text = text or self.text
        self.tag = tag or self.tag
        self.command = command or self.command
        self.description = description or self.description
        self.start_position = start_position or self.start_position
        self.count = count or self.count
        self.min_value = min_value or self.min_value
        self.max_value = max_value or self.max_value
        self.none_value = none_value or self.none_value
        if modules:
            modules = [x for x in Module.query.all() if x.id in json.loads(modules)]
            self.modules = modules if len(modules) else self.modules
        else:
            self.modules = self.modules

    def __str__(self):
        return json.dumps({
            "name": self.name,
            "text": self.text,
            "command": self.command,
            "tag": self.tag,
            "description": self.description,
            "start_position": self.start_position,
            "count": self.count,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "none_value": self.none_value,
            "modules": [x.name for x in self.modules],
        })

    def __repr__(self):
        return str(self)
