import bcrypt


class User():

    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection
        self.quit = False

    def login(self):
        print(
            f"\nTo login, please enter your email and password.\nPress 'Q' to quit.")
        while True:
            email = input(f"\nEmail: ")
            password = input(f"Password: ").encode()
            if email.upper() == 'Q' or password.upper() == 'Q':
                print("\nHave a nice day!")
                return
            try:
                query = f"SELECT * FROM Users WHERE email = '{email}'"
                information = self.cursor.execute(query).fetchall()
                user = []
                for info in information:
                    user = [i for i in info]
                if bcrypt.checkpw(password, user[4]):
                    print(f"\nHello, {user[1]} {user[2]}!")
                    if user[8] == 'Manager':
                        return user[8]
                    else:
                        self.user = user
                        self.user[4] = password.decode()
                        break
                else:
                    print("\nIncorrect password.")
            except:
                print("\nUsername or Password incorrect. Please try again.")
        self.nav_user()

    def nav_user(self):
        while self.quit == False:
            print(
                f"\n*Welcome to the user navigation menu.*\n\nPlease select from the following options:")
            action = input("(1) View assessment data\n(2) Edit user information\n(0) Quit\n>>> ")
            if action == '1':
                self.view_data(self.user)
            elif action == '2':
                self.edit_data(self.user)
            elif action == '0':
                self.quit_menu()
            else:
                print("\nInvalid input.")
    
    def view_data(self,user):
        print(f"\nAssessment Data for {user[1]} {user[2]}:")
        query = """SELECT a.assessment_name, a.competency_name, ar.score, ar.date_taken 
        FROM Assessment_Results ar JOIN Assessments a ON a.assessment_id = ar.assessment_id WHERE ar.user_id = ?"""
        value = (user[0],)
        assessment_data = self.cursor.execute(query,value).fetchall()
        print(f"\n{'Assessment Name':<30}{'Competency Name':<20}{'Score':<8}{'Date Taken':<15}\n{'-'*70}")
        if assessment_data == []:
            print("No current assessments for this user")
        else:
            for data in assessment_data:
                print(f"{data[0]:<30}{data[1]:<20}{data[2]:<8}{data[3]:<15}")
        action = input("\nPress 'Q' to quit or <enter> to return to the navigation menu. ")
        if action.upper() == "Q":
            self.quit_menu()
        else:
            return

    def edit_data(self, user):
        while True:
            query1 = f"SELECT user_id, first_name, last_name, phone, password, email FROM Users WHERE user_id = {user[0]}"
            user_info = self.cursor.execute(query1).fetchall()
            for user in user_info:
                print(f"\nCurrent user information for {user[1]} {user[2]}:")           
                print(f"\n{'ID':<7}{'First Name':<15}{'Last Name':<15}{'Phone':<14}{'Email':<30}\n{'-'*90}")
                print(f"{user[0]:<7}{user[1]:<15}{user[2]:<15}{user[3]:<14}{user[5]:<30}")
            change = input(f"\nWhat would you like to update?\n(1) First name\n(2) Last Name\n(3) Phone Number\n(4) Password or\n(5) Email or\n(0) To return to navigation\n>>> ")
            if change == '0':
                return
            user_dic = dict(zip([1,2,3,4,5], ['first_name', 'last_name', 'phone', 'password', 'email']))
            try:
                change = int(change)
            except:
                print("\nInvalid input")
                continue
            if change == 4:
                password = input(
                f"New password: ").encode()
                hashed = bcrypt.hashpw(password, bcrypt.gensalt())
                try:
                    query2 = f"UPDATE Users SET password = ? WHERE user_id = ?"
                    values2 = (hashed, user[0])
                    self.cursor.execute(query2, values2)
                    self.connection.commit()
                    print(f"\nAccount succesfully updated!")
                except:
                    print(f"That password already exists.")
            else:
                if change in user_dic.keys():
                    change_to = input(f"\nWhat would you like to change ({change}) to? ")          
                    query2 = f"UPDATE Users SET {user_dic[change]} = ? WHERE user_id = ?"
                    values2 = (f'{change_to}', user[0])
                    self.cursor.execute(query2, values2)
                    self.connection.commit()
                    print(f"\nAccount succesfully updated!")
                else:
                    print("\nInvalid input")
            action = input("\nPress 'C' to make another change or <enter> to return to the navigation menu. ")
            if action.upper() == "C":
                continue
            else:
                break
        return

    def quit_menu(self):
        print("\nHave a nice day!\n")
        self.quit = True


