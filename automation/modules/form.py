from wtforms import Form, StringField, validators


class ModuleForm(Form):
    name = StringField("Module name", [validators.DataRequired()])
    text = StringField("Module Text", [validators.DataRequired()])
    description = StringField("Module description")
    sending_data = StringField("Sending data")
