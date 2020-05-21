import populatingTables, resumeGenerator
import pyodbc
connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=DESKTOP-BBOOHAU\MSSQLSERVER01;'
                      'Database=Client;'
                      'Trusted_Connection=yes;')

def activity(memberID):
    while(1):
        print("1. View Details\n2. Generate Resume\n3. Log Out")
        choice = int(input("Enter choice : "))
        if choice not in [1, 2, 3]:
            print("Invalid choice! Try again.")
        else:
            if choice == 1:
                populatingTables.displayDetails(memberID)
            elif choice == 2:
                values = populatingTables.clientInfo(memberID)
                resume_values = populatingTables.structureDetails(values)
                resumeGenerator.create_resume(resume_values)  
            else:
                return

def run():
    while(1):
        print("1. Register\n2. Log In\n3. Exit")
        choice = int(input("Enter choice : "))
        if choice not in [1, 2, 3]:
            print("Invalid choice! Try again")
        else:
            if choice == 1:
                memberID = populatingTables.registerAccount()
                activity(memberID)
            elif choice == 2:
                memberID = input("Enter member ID : ")
                password = input("Enter password : ")
                cur = connection.cursor()
                check_login = cur.execute("SELECT NAME FROM MEMBER WHERE MEMBER_ID = ? AND PASSWORD = ?", (memberID, password)).fetchall()
                if not check_login:
                    print("Error! Member does not exist!")
                    run()
                else:
                    activity(memberID)
            else:
                break
                
if __name__ == "__main__":
    run()
    connection.close()