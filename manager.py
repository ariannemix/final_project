from add_record import addRecord
from view_record import viewRecord
from edit_record import editRecord
from manage_files import manageFiles
from user import User


class Manager(User):

    def __init__(self, cursor, connection):
        super().__init__(cursor, connection)

    def nav_manager(self):
        while self.quit == False:
            print(
                f"\n*Welcome to the Manager navigation menu.*\n\nPlease select from the following options:")
            action = input("(1) View Data\n(2) Search for Records\n(3) Add a record\n"
                           "(4) Manage files\n(5) Edit a record\n(6) Delete an Assessment Result\n"
                           "(0) Quit\n>>> ")
            if action == '1':
                self.view_data()
            elif action == '2':
                self.search_users()
            elif action == '3':
                self.add_record()
            elif action == '4':
                self.manage_files()
            elif action == '5':
                self.edit_record()
            elif action == '6':
                self.delete_result()
            elif action == '0':
                self.quit_menu()

    def add_record(self):
        add_record = addRecord(self.cursor, self.connection)
        action = input("\nPlease indicate the type of record you would like to add:\n(1) Add a user\n"
                       "(2) Add a new competency\n(3) Add a new competency assessment\n(4) Add a test result for a user\n"
                       "(0) Return to main menu\n>>> """)
        if action == '0':
            return
        elif action == '1':
            add_record.add_user()
        elif action == '2':
            add_record.add_competency()
        elif action == '3':
            add_record.add_assessment()
        elif action == '4':
            add_record.add_test_result()
        else:
            print("\n**Invalid Response**")

        self.navigate()

    def view_data(self):
        view_record = viewRecord(self.cursor, self.connection)
        action = input("\nWhich records would you like to view?\n(1) Competencies and results for a given user\n"
                       "(2) Assessments for a given user\n(3) Complete list of user results for a given competency\n(4) Complete list of users\n>>> ")
        if action == '1':
            view_record.view_one_user_competency()
        elif action == '2':
            view_record.view_one_user_assessments()
        elif action == '3':
            view_record.view_by_competency()
        elif action == '4':
            view_record.view_users()
        else:
            print("\nInvalid input")
        self.navigate()

    def edit_record(self):
        edit_record = editRecord(self.cursor, self.connection)

        action = input("\nWhich records would you like to edit?\n(1) User information\n"
                       "(2) An Assessment Name \n(3) An Assessment Result\n>>> ")
        if action == '1':
            user = edit_record.edit_user()
            if user == None:
                return
            self.edit_data(user)
            return
        elif action == '2':
            edit_record.edit_assessment()
        elif action == '3':
            edit_record.update_result()
        else:
            print("\nInvalid input")
        self.navigate()

    def delete_result(self):
        query = """SELECT ar.result_id, u.first_name, u.last_name, ar.score, a.assessment_name 
        FROM Assessment_Results ar JOIN Assessments a ON a.assessment_id = ar.assessment_id 
        JOIN Users u ON u.user_id = ar.user_id """
        assessment_info = self.cursor.execute(query).fetchall()
        result_ids = []
        print(f"\n{'Result ID':<12}{'First Name':<15}{'Last Name':<15}{'Score':<8}{'Assessment Name':<30}\n{'-'*70}")
        if assessment_info == []:
            print(f"No current assessments for this competency")
            return
        for assessment in assessment_info:
            print(
                f"{assessment[0]:<12}{assessment[1]:<15}{assessment[2]:<15}{assessment[3]:<8}{assessment[4]:<15}")
            result_ids.append(assessment[0])
        result_id = input(
            "\nEnter the ID of the assessment you would like to delete (or <enter> to return to navigation menu): ")
        if result_id == '':
            return
        try:
            result_id = int(result_id)
        except:
            print("\nInvalid ID")
            return
        if result_id in result_ids:
            query = "DELETE FROM Assessment_Results WHERE result_id = ?"
            value = (result_id,)
            self.cursor.execute(query, value)
            self.connection.commit()
            print("\nResult successfully deleted.")
        else:
            print(f"\nInvalid ID")
        self.navigate()

    def manage_files(self):
        manage_files = manageFiles(self.cursor, self.connection)

        action = input("\nWhat would you like to do?\n(1) Create a competency report\n"
                       "(2) Import assessment results\n>>> ")
        if action == '1':
            manage_files.create_report()
        elif action == '2':
            manage_files.import_results()
        else:
            print("\nInvalid input")
        self.navigate()

    def search_users(self):
        name = input(
            f"Enter the first or last name of the person whose profile you would like to view: ")
        query = "SELECT user_id, first_name, last_name, phone, email, date_created FROM Users WHERE first_name LIKE ? OR last_name LIKE ?"
        values = (f"%{name}%", f"%{name}%")
        try:
            user = self.cursor.execute(query, values).fetchall()
        except:
            print(
                f"\nSorry, it looks like {name} isn't in the database. Check you spelling and try again.")
        print(f"\n{'ID':<7}{'First Name':<15}{'Last Name':<15}{'Phone':<14}{'Email':<30}{'Date Created':<12}\n{'-'*100}")
        for info in user:
            print(
                f"{info[0]:<7}{info[1]:<15}{info[2]:<15}{info[3]:<14}{info[4]:<30}{info[5]:<12}")
        self.navigate()

    def navigate(self):
        action = input(
            "\nPress 'Q' to quit, or <enter> to return to the manager navigation menu.\n>>> ")
        if action.upper() == 'Q':
            self.quit_menu()
        else:
            return
