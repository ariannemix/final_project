
import sqlite3
from manage_files import manageFiles

from user import User
from manager import Manager
from edit_record import editRecord
from manage_files import manageFiles

connection = sqlite3.connect('competencies.db')
cursor = connection.cursor()


user = User(cursor, connection)
user_type = user.login()
if user_type == 'Manager':
    manager = Manager(cursor, connection)
    manager.nav_manager()

