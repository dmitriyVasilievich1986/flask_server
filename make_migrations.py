from automation.application.database import db
from automation.application.app import create_app
from automation.modules import Module
from automation.command import Command
from automation.rs485 import RS485
from automation.Test import Test
from automation.automation.automation import Automation

db.create_all()
