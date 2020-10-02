from ..application.database import db
import json


class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    text = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    sending_data = db.Column(db.String(200))
    bayan_module = db.relationship("RS485", backref='module', lazy=True)

    def __init__(self, name=None, text=None, description=None, sending_data=None):
        self.name = name or self.name
        self.text = text or self.text
        self.description = description or self.description
        if sending_data:
            self.sending_data = (
                sending_data
                if isinstance(sending_data, str) or isinstance(sending_data, unicode)
                else json.dumps(sending_data)
            )
        else:
            self.sending_data = self.sending_data

    def __str__(self):
        return json.dumps({
            "name": self.name,
            "text": self.text,
            "description": self.description,
            "sending_data": json.loads(self.sending_data) if self.sending_data else "",
            "bayan_modules": [b_module.name for b_module in self.bayan_module],
        })
