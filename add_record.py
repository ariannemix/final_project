from helpers import get_time
import bcrypt


class addRecord:

    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    def add_user(self):
        print(f"\nPlease complete the following information to add a new user. Press <enter> to skip a field.\n**The fields marked with '*' are required.**\n")
        date_created = get_time()
        first_name = input(f"{'First Name*':<12}: ").title()
        last_name = input(f"{'Last Name*':<12}: ").title()
        phone = input(f"{'Phone':<12}: ")
        email = input(f"{'Email*':<12}: ")
        password = input(
            f"Password (must be at least 8 characters in length): ").encode()
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        user_type = input(f"Is this person a manager? (Y/N): ").upper()
        user_type = 'Manager' if user_type == 'Y' else 'User'
        try:
            query = f"INSERT INTO Users (first_name, last_name, phone, email, password, user_type, date_created) VALUES (?,?,?,?,?,?,?)"
            values = (first_name, last_name, phone,
                      email, hashed, user_type, date_created)
            self.cursor.execute(query, values)
            self.connection.commit()
            print(
                f"\n{first_name} {last_name} has been successfully added as a {user_type}.")
        except:
            print(f"\nEmails and Passwords must be unique. Please try again later.")
    

    def add_competency(self):
        date_created = get_time()
        name = input(
            "\nPlease enter the name of the competency you would like to add: ")
        query = "INSERT INTO Competencies (date_created, name) VALUES (?,?)"
        values = (date_created, name)
        self.cursor.execute(query, values)
        self.connection.commit()
        print(f"\nCompetency {name} successfully added.")

    def add_assessment(self):
        print("\nPlease enter the ID of the competency to be tested from the following list")
        query = "SELECT competency_id, name FROM Competencies"
        competencies = self.cursor.execute(query).fetchall()
        print(f"\n{'ID':<5}{'Competency Name':<30}\n{'-'*40}")
        for competency in competencies:
            print(f"{competency[0]:<5}{competency[1]:<30}")
        competency_id = input(f">>> ")
        try:
            competency_id = int(competency_id)
        except:
            print("Invalid ID")
            return
        for competency in competencies:
            if competency[0] == competency_id:
                competency_id = competency[1]
                break
        date_created = get_time()
        assessment_name = input("\nPlease enter the name of the competency assessment you would like to add: ").title()
        query2 = "INSERT INTO Assessments (assessment_name, date_created, competency_name) VALUES (?,?,?)"
        values = (assessment_name, date_created, competency_id)
        self.cursor.execute(query2, values)
        self.connection.commit()
        print(f"\n{assessment_name} has successfully been added to available assessments.")

        
    def add_test_result(self):
        print(f"\nPlease enter the ID of the person whose assessment you'd like to update.")
        print(f"\n{'ID':<5}{'Name':<30}\n{'-'*40}")
        query = "SELECT user_id, first_name, last_name FROM Users"
        users = self.cursor.execute(query).fetchall()
        user_ids = []
        assessment_ids = []
        for user in users:
            print(f"{user[0]:<5}{user[1] + ' ' + user[2]:<30}")
            user_ids.append(user[0])
        assessed_user = input(f">>> ")
        manager_id = input(f"\nPlease enter the ID of the manager who administered the test. If no manager was involved, press <enter>.\n>>> ")
        if manager_id != '':
            try: 
                manager_id = int(manager_id)
                if manager_id not in user_ids:
                    print(f"\nInvalid ID")
                    return
            except:
                print("\nInvalid ID")
                return
        print(f"\nPlease enter the ID of the assessment you'd like to add.")
        print(f"\n{'ID':<5}{'Name':<30}\n{'-'*40}")
        query = "SELECT assessment_id, assessment_name FROM Assessments"
        assessments = self.cursor.execute(query).fetchall()
        for assessment in assessments:
            print(f"{assessment[0]:<5}{assessment[1]:<30}")
            assessment_ids.append(assessment[0])
        assessment_id = input(f">>> ")
        try:
            assessment_id = int(assessment_id)
            assessed_user = int(assessed_user)
        except:
            print("\nInvalid ID(s)")
            return
        if assessment_id in assessment_ids and assessed_user in user_ids:
            date_taken = get_time()
            score = input(f"Please enter the score (1-5): ")
            if manager_id != '' and manager_id in user_ids:
                query = "INSERT INTO Assessment_Results (user_id, assessment_id, score, date_taken, manager_id) VALUES(?,?,?,?,?)"
                values = (assessed_user, assessment_id, score, date_taken, manager_id)
            else:
                query = "INSERT INTO Assessment_Results (user_id, assessment_id, score, date_taken) VALUES(?,?,?,?)"
                values = (assessed_user, assessment_id, score, date_taken)
            self.cursor.execute(query, values)
            self.connection.commit()
            print(f"\nAssessment score successfully added.")
        else:
            print(f"\nEither the assessment ID or the user ID you provided is incorrect. Please check your information and try again.")