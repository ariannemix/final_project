
import sqlite3

from user import User
from manager import Manager
from edit_record import editRecord

connection = sqlite3.connect('competencies.db')
cursor = connection.cursor()


user = User(cursor, connection)
user_type = user.login()
if user_type == 'Manager':
    manager = Manager(cursor, connection)
    manager.nav_manager()
