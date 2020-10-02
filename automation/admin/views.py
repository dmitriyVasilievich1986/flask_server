from flask import Blueprint, request, render_template
from ..modules import Module, ModuleForm
from ..application.database import db

admin_api = Blueprint("admin_api", __name__, template_folder="templates")


@admin_api.route("/module", methods=["GET", "POST"])
def module_view():
    form = ModuleForm(request.form)
    if request.method == "POST" and form.validate():
        try:
            module = Module(form.name.data, form.text.data, form.description.data, form.sending_data.data)
            db.session.add(module)
            db.session.commit()
        except BaseException:
            return "Can`t create Bad request data."
        return "OK"
    return render_template("index.html", form=form)
