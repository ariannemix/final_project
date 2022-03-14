class editRecord():

    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection
        self.user_ids = []

    def edit_user(self):
        query = "SELECT * FROM Users"
        users = self.cursor.execute(query)
        print(f"\n{'ID':<7}{'First Name':<15}{'Last Name':<15}{'Phone':<14}{'Email':<30}{'Date Created':<12}\n{'-'*100}")
        for user in users:
            print(f"{user[0]:<7}{user[1]:<15}{user[2]:<15}{user[3]:<14}{user[5]:<30}{user[7]:<12}")
            if user[0] not in self.user_ids:
                self.user_ids.append(user[0])
        action = input("\nEnter the ID of the user whose account you would like to edit: ")
        try:
            action = int(action)
        except:
            print("\nInvalid ID")
            return
        if action not in self.user_ids:
            print("\nInvalid user ID.")
            return 
        query = "SELECT * FROM Users WHERE user_id = ?"
        value = (action,)
        users = self.cursor.execute(query,value)
        if users == []:
            return
        for user in users:
            user = [i for i in user]
            return user

    def edit_assessment(self):
        query = "SELECT * FROM Assessments"
        assessments = self.cursor.execute(query).fetchall()
        print(f"\n{'ID':<8}{'Assessment Name':<30}{'Date Created':<15}{'Competency Name':<20}\n{'-'*80}")
        for assessment in assessments:
            print(f"{assessment[0]:<8}{assessment[1]:<30}{assessment[3]:<15}{assessment[2]:<20}")
        action = input("\nEnter the ID of the assessment you would like to edit: ")
        try:
            action = int(action)
        except:
            print("\nInvalid ID")
            return 
        new_name = input("What would you like to change the assessment name to? ").title()
        try:
            query = "UPDATE Assessments SET assessment_name = ? WHERE assessment_id = ?"
            value = (new_name,action)
            self.cursor.execute(query,value)
            self.connection.commit()
            print(f"\nAssessment name successfully updated!")
        except:
            print(f"\nInvalid assessment ID.")

    def update_result(self):
        query = """SELECT ar.result_id, u.first_name, u.last_name, ar.score, a.assessment_name 
        FROM Assessment_Results ar JOIN Assessments a ON a.assessment_id = ar.assessment_id 
        JOIN Users u ON u.user_id = ar.user_id """
        assessment_info = self.cursor.execute(query).fetchall()
        result_ids=[]
        print(f"\n{'Result ID':<12}{'First Name':<15}{'Last Name':<15}{'Score':<8}{'Assessment Name':<30}\n{'-'*70}")
        if assessment_info == []:
            print(f"No current assessments for this competency")
            return
        for assessment in assessment_info:
            print(f"{assessment[0]:<12}{assessment[1]:<15}{assessment[2]:<15}{assessment[3]:<8}{assessment[4]:<15}")
            result_ids.append(assessment[0])
        result_id = input("\nEnter the ID of the assessment you would like to edit: ")
        try:
            result_id = int(result_id)
        except:
            print("\nInvalid ID")
            return 
        if result_id in result_ids:
            action = input(f"What would you like to change the scores to? (1-5) ")
            try:
                action = int(action)
            except:
                print("\nInvalid Score")
                return 
        query = "UPDATE Assessment_Results SET score = ? WHERE result_id = ?"
        value = (action, result_id)
        self.cursor.execute(query,value)
        self.connection.commit()
        print(f"\nScore successfully updated!")

    # edit a user's information
        # edit a competency; I don't think this should be an option because results and assessments depend on competency. 
        # edit an assessment
        # edit an assessment result