class viewRecord:

    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection
        self.user_ids = []

    def view_users(self):
        query = "SELECT user_id, first_name, last_name, phone, email, date_created FROM Users"
        users = self.cursor.execute(query)
        print(f"\n{'ID':<7}{'First Name':<15}{'Last Name':<15}{'Phone':<14}{'Email':<30}{'Date Created':<12}\n{'-'*100}")
        for user in users:
            print(f"{user[0]:<7}{user[1]:<15}{user[2]:<15}{user[3]:<14}{user[4]:<30}{user[5]:<12}")
            if user[0] not in self.user_ids:
                self.user_ids.append(user[0])

    def view_one_user_competency(self):
        self.view_users()
        action = input("\nEnter the ID of the user whose competencies you would like to view: ")
        try:
            action = int(action)
        except:
            print("\nInvalid ID")
            return
        if action not in self.user_ids:
            print("\nInvalid ID")
            return
        query = """SELECT a.assessment_name, a.competency_name, ar.score, ar.date_taken 
        FROM Assessment_Results ar JOIN Assessments a ON a.assessment_id = ar.assessment_id WHERE ar.user_id = ?"""
        value = (action,)
        assessment_data = self.cursor.execute(query,value).fetchall()
        print(f"\n{'Assessment Name':<30}{'Competency Name':<20}{'Score':<8}{'Date Taken':<15}\n{'-'*60}")
        if assessment_data == []:
            print("No current assessments for this user")
        else:
            for data in assessment_data:
                print(f"{data[0]:<30}{data[1]:<20}{data[2]:<8}{data[3]:<15}")

    def view_by_competency(self):
        query = "SELECT * FROM Competencies"
        competencies = self.cursor.execute(query).fetchall()
        print(f"\n{'Competency ID':<5}{'Competency Name':<30}{'Date Created':<14}\n{'-'*60}")
        competency_ids = []
        for competency in competencies:
            print(f"{competency[0]:<5}{competency[1]:<30}{competency[2]:<14}")
            competency_ids.append(competency[0])
        action = input("\nEnter the ID of the competency whose user scores you would like to view: ")
        try:
            action = int(action)
        except:
            print("\nInvalid ID")
            return
        if action not in competency_ids:
            print("\nInvalid ID")
            return
        query = """SELECT c.name, u.first_name, u.last_name, ar.score, a.assessment_name 
        FROM Assessment_Results ar JOIN Assessments a ON a.assessment_id = ar.assessment_id 
        JOIN Users u ON u.user_id = ar.user_id 
        JOIN Competencies c ON c.name = a.competency_name 
        WHERE c.competency_id = ?"""
        value = (action,)
        assessment_info = self.cursor.execute(query,value).fetchall()
        if assessment_info == []:
            print(f"\nNo current assessments for this competency")
            return
        for assessment in assessment_info:
            print(f"\nScores for {assessment_info[0][0]} competency:")
            print(f"\n{'First Name':<15}{'Last Name':<15}{'Score':<8}{'Assessment Name':<30}\n{'-'*70}")
            print(f"{assessment[1]:<15}{assessment[2]:<15}{assessment[3]:<8}{assessment[4]:<15}")

    def view_one_user_assessments(self):
        self.view_users()
        action = input("\nEnter the ID of the user whose assessments you would like to view: ")
        try:
            action = int(action)
        except:
            print("\nInvalid ID")
            return
        if action not in self.user_ids:
            print("\nInvalid ID")
            return
        query = """SELECT a.assessment_name, u.first_name, u.last_name 
                FROM Assessment_Results ar
                JOIN Assessments a ON a.assessment_id = ar.assessment_id
                JOIN Users u ON u.user_id = ar.user_id
                WHERE ar.user_id = ?"""
        value = (action,)
        assessments = self.cursor.execute(query, value).fetchall()
        print(f"\n{'Assessment Name':<30}{'User Name':<30}\n{'-'*70}")
        if assessments == []:
            print("No current assessments for this user")
        else:
            for assessment in assessments:
                print(f"{assessment[0]:<30}{assessment[1] + ' ' + assessment[2]:<30}")
