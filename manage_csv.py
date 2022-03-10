import csv

class manageCSV():

    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    def import_results(self):
        pass

    def create_report(self):
        action = input("\nWould you like to:\n(1) Create a competency report for a single user or\n(2) Create a competency report for all users\n>>> ")
        if action == '1':
            query = "SELECT * FROM Users"
            users = self.cursor.execute(query)
            print(f"\n{'ID':<7}{'First Name':<15}{'Last Name':<15}{'Phone':<14}{'Email':<30}{'Date Created':<12}\n{'-'*100}")
            for user in users:
                print(f"{user[0]:<7}{user[1]:<15}{user[2]:<15}{user[3]:<14}{user[5]:<30}{user[7]:<12}")
            action = input("\nEnter the ID of the user you'd like to include in the report: ")
            try:
                action = int(action)
            except:
                print("\nInvalid ID")
                return
            try:
                query = """SELECT a.competency_name, a.assessment_name, ar.score, ar.date_taken, u.last_name
                        FROM Assessment_Results ar
                        JOIN Assessments a ON a.assessment_id = ar.assessment_id
                        JOIN Users u ON u.user_id = ar.user_id
                        WHERE ar.user_id = ?"""
                value = (action,)
                user_information = self.cursor.execute(query,value).fetchall()
                for info in user_information:
                    user_info = [i for i in info]
                name = user_info[-1]
                header = ['Competency','Assessment', 'Score','Date_Taken']
                l = [dict(zip(header, user_info))] 
                self.create_csv(l, header, name.lower())
            except:
                print("\nInvalid ID")
        elif action == '2':
            query = """SELECT ar.user_id, a.assessment_id, ar.score, ar.date_taken
                        FROM Assessment_Results ar
                        JOIN Assessments a ON a.assessment_id = ar.assessment_id"""
            information = self.cursor.execute(query).fetchall()
            header = ['user_id', 'Assessment ID', 'Score','Date_Taken']
            l = []
            for info in information:
                user_info = [i for i in info]             
                obj = dict(zip(header, user_info)) 
                l.append(obj)      
            self.create_csv(l, header)
        else:
            print("\nInvalid input.")
       

    def create_csv(self, obj, header, name='allusers'):

        with open(f"{name}competency.csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=header)
            writer.writeheader()
            writer.writerows(obj)

        print(f"\nCSV file, {name}competency.csv, successfully created.")

    def import_results(self):
        file = input("What is the file's name? ")
        with open(f"{file}", 'r') as csvfile:
            lines = csv.reader(csvfile)
            header = next(lines)
            for line in lines:
                query = "INSERT INTO Assessment_Results (user_id,assessment_id,score,date_taken) VALUES (?,?,?,?)"
                values = (line[0],line[1],line[2],line[3])
                self.cursor.execute(query,values)
                self.connection.commit()
                print(f"\nResults successfully imported.")

#                 user_id,Competency,Assessment ID,Score,Date_Taken
# 2,Boolean Logic,4,5,2022-03-07
       # EXPORT
        # Competency report by competency and users
        # Competency report for a single user
        # IMPORT
        # The ability to import assessment results from a CSV file
        # The CSV file would contain columns user_id, assessment_id, score, date_taken