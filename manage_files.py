import csv
from helpers import get_time
from fpdf import FPDF



class manageFiles():

    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    def import_results(self):
        pass

    def create_report(self):
        action = input(
            "\nWould you like to:\n(1) Create a competency report for a single user or\n(2) Create a competency report for all users\n>>> ")
        if action == '1':
            query = "SELECT * FROM Users"
            users = self.cursor.execute(query)
            print(
                f"\n{'ID':<7}{'First Name':<15}{'Last Name':<15}{'Phone':<14}{'Email':<30}{'Date Created':<12}\n{'-'*100}")
            for user in users:
                print(
                    f"{user[0]:<7}{user[1]:<15}{user[2]:<15}{user[3]:<14}{user[5]:<30}{user[7]:<12}")
            action = input(
                "\nEnter the ID of the user you'd like to include in the report: ")
            try:
                action = int(action)
            except:
                print("\nInvalid ID")
                return
            try:
                query = """SELECT a.competency_name, a.assessment_name, ar.score, ar.date_taken, u.first_name, u.last_name
                        FROM Assessment_Results ar
                        JOIN Assessments a ON a.assessment_id = ar.assessment_id
                        JOIN Users u ON u.user_id = ar.user_id
                        WHERE ar.user_id = ?"""
                value = (action,)
                user_information = self.cursor.execute(query, value).fetchall()
                if user_information == []:
                    print(f"\nThere is no assessment report for this user.")
                    return
                header = ['Competency', 'Assessment', 'Score', 'Date_Taken']
                l = []
                name = []
                for info in user_information:
                    user_info = [i for i in info]
                    obj = dict(zip(header, user_info))
                    l.append(obj)
                    name = user_info[-2:]
                report_type = input(
                    f"Would you like to create \n(1) A pdf file or \n(2) A csv file?\n>>> ")
                if report_type == '1':
                    self.create_pdf(l, header, name)
                    return
                elif report_type == '2':
                    self.create_csv(l, header, name)
                    return
                else:
                    print(f"\nInvalid input.")
                    return
            except:
                print("\nInvalid ID")
        elif action == '2':
            query = """SELECT ar.user_id, a.assessment_id, ar.score, ar.date_taken
                        FROM Assessment_Results ar
                        JOIN Assessments a ON a.assessment_id = ar.assessment_id"""
            information = self.cursor.execute(query).fetchall()
            header = ['user_id', 'assessment_id', 'score', 'date_taken']
            l = []
            for info in information:
                user_info = [i for i in info]
                obj = dict(zip(header, user_info))
                l.append(obj)
            report_type = input(
                f"Would you like to create \n(1) A pdf file or \n(2) A csv file?\n>>> ")
            if report_type == '1':
                self.create_pdf(l, header)
                return
            elif report_type == '2':
                self.create_csv(l, header)
                return
            else:
                print(f"\nInvalid input.")
                return
        else:
            print("\nInvalid input.")

    def create_csv(self, obj, header, name='allusers'):

        with open(f"{''.join(name).lower()}competency.csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=header)
            writer.writeheader()
            writer.writerows(obj)

        print(f"\nCSV file, {''.join(name).lower()}competency.csv, successfully created.")

    def import_results(self):
        file = input("What is the file's name? ")
        with open(f"{file}", 'r') as csvfile:
            lines = csv.reader(csvfile)
            header = next(lines)
            for line in lines:
                query = "INSERT INTO Assessment_Results (user_id,assessment_id,score,date_taken) VALUES (?,?,?,?)"
                values = (line[0], line[1], line[2], line[3])
                self.cursor.execute(query, values)
                self.connection.commit()
                print(f"\nResults successfully imported.")

    def create_pdf(self, obj, header, name=['All','Users']):
        time = get_time()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('helvetica', size=18)
        text = f"Competency Report for {' '.join(name)}:"
        pdf.cell(w=200, txt=text, ln=1, align='c')
        pdf.set_font('helvetica', size=12)
        for i in range(0, len(obj)):
            pdf.cell(txt=f'REPORT NUMBER {i+1}:', ln=1, align='')
            for x in range(0,len(header)):
                text = f"{header[x]}: {obj[i][header[x]]} | "
                pdf.cell(txt=text)
                if x == 3:
                    pdf.cell(w=1,txt='',ln=1)
        if name == ['All','Users']:
            pdf.output(f'competency{time}.pdf')
        else:
            pdf.output(f'{name[1].lower()}competency.pdf')
        print(f"\nPDF file successfully created.")


