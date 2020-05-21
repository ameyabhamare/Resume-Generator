import pyodbc
import re
from datetime import date
import resumeGenerator

connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=DESKTOP-BBOOHAU\MSSQLSERVER01;'
                      'Database=Client;'
                      'Trusted_Connection=yes;')

def createMember():
    cur = connection.cursor()

    memberList = cur.execute("SELECT MEMBER_ID FROM MEMBER").fetchall()
    if memberList == []:
        memberCount = 1
    else:
        mList = [i[0] for i in memberList]
        memberCount = int(max(mList)[4:10]) + 1
    memberID = "MEM#" + str(memberCount).zfill(6)
    
    name = input("Name : ")
    while not all(x.isalpha() or x == "" or x == " " for x in name):
        print("Invalid format. Please enter a valid name.")
        name = input("Name : ")

    password = input("Password (At least 8 characters long) : ")
    while len(password) < 8:
        print("Invalid format. Password has to be atleast 8 characters long.")
        password = input("Password: ")

    email = input("Email ID : ")
    pattern = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    while not(re.search(pattern, email)):
        print("Invalid format. Please enter a valid email address.")
        email = input("Email ID : ")

    phone = input("Phone : ")
    while not(phone.isdigit() and len(phone) == 10):
        print("Invalid format. Please enter valid 10 digit phone number.")
        phone = input("Phone : ")

    address = input("Residential Address : ")

    bio = input("Enter bio : ")

    gitHub = input("Enter Github URL : ")

    linkedIn = input("Enter LinkedIn URL : ")

    cur.execute("INSERT INTO MEMBER VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (memberID, password, name, email, phone, address, bio, gitHub, linkedIn))

    connection.commit()
    cur.close()

    return memberID

def school():
    cur = connection.cursor()

    schoolName = input("School name : ").upper()
    while not all(x.isalpha() or x == "" or x == " " for x in schoolName):
        print("Invalid format. Please enter valid school name.")
        schoolName = input("School name : ").upper()
    
    location = input("Location of school : ").upper()
    while not all(x.isalnum() or x == "" or x == " " for x in location):
        print("Invalid format. Please enter valid location.")
        location = input("Location of school : ").upper()

    checkSchool = cur.execute("SELECT NAME FROM SCHOOL WHERE NAME = ? AND LOCATION = ?", (schoolName, location)).fetchall()
    if checkSchool == []:
        schoolList = cur.execute("SELECT SCHOOL_ID FROM SCHOOL").fetchall()
        if schoolList == []:
            schoolCount = 1
        else:
            #print(schoolList)
            sList = [i[0] for i in schoolList]
            #print(schoolList)
            schoolCount = int(max(sList)[4:10]) + 1
            #print(schoolCount)
        schoolID = "SCH#" + str(schoolCount).zfill(6)
        cur.execute("INSERT INTO SCHOOL VALUES (?, ?, ?)", (schoolID, location, schoolName))
    else:
        schoolID = cur.execute("SELECT SCHOOL_ID FROM SCHOOL WHERE NAME = ? AND LOCATION = ?", (schoolName, location)).fetchall()[0][0]
    
    connection.commit()
    cur.close()

    return schoolID

def schooling(memberID):
    cur = connection.cursor()

    for passingLevel in [10, 12]:
        schoolID = school()

        stream = input("Enter stream (Science, Commerce, Arts or Humanities) : " )
        while stream not in ['Science', 'Commerce', 'Arts', 'Humanities']:
            print("Invalid format. Please enter valid stream.")
            stream = input("Enter stream (Science, Commerce, Arts or Humanities) : ")

        passingYear = int(input("Enter passing year : "))
        while not(len(str(passingYear)) == 4):
            print("Invalid format. Please enter valid passing year.")
            passingYear = int(input("Enter passing year : "))

        score = float(input("Enter percentage : "))
        while not(0.0 <= score <= 100.0):
            print("Invalid format. Please enter valid score.")
            score = float(input("Enter percentage : "))
        
        cur.execute("INSERT INTO SCHOOLING VALUES (?, ?, ?, ?, ?, ?)", (memberID, schoolID, passingLevel, stream, passingYear, score))

    connection.commit()
    cur.close()

def degreeInfo(typeGraduation, degree, major):  
    cur = connection.cursor()

    checkDegree = cur.execute("SELECT TYPE_OF_GRADUATION FROM DEGREE_INFO WHERE TYPE_OF_GRADUATION = ? AND DEGREE = ? AND MAJOR = ?", (typeGraduation, degree, major)).fetchall()
    if checkDegree == []:
            degreeList = cur.execute("SELECT DEGREE_ID FROM DEGREE_INFO").fetchall()
            if degreeList == []:
                degreeCount = 1
            else:
                dList= [i[0] for i in degreeList]
                degreeCount = int(max(dList)[4:10]) + 1
            degreeID = "DEG#" + str(degreeCount).zfill(6)
            cur.execute("INSERT INTO DEGREE_INFO VALUES (?, ?, ?, ?)", (degreeID, typeGraduation, degree, major))
    else:
            degreeID = cur.execute("SELECT DEGREE_ID FROM DEGREE_INFO WHERE TYPE_OF_GRADUATION = ? AND DEGREE = ? AND MAJOR = ?", (typeGraduation, degree, major)).fetchall()[0][0]

    connection.commit()
    cur.close()

    return degreeID
        
def higherEducation(memberID):
    cur = connection.cursor()

    f = 1
    while f == 1:
        typeGraduation = input("Enter type of graduation i.e. (Bachelor's / Master's / Doctorate) : ").upper()
        while not all(x.isalpha() or x == "" or x == "'" for x in typeGraduation):
            print("Invalid format. Please enter valid type of graduation.")
            typeGraduation = input("Enter type of graduation i.e. (Bachelor's / Master's / Doctorate)")

        degree = input("Enter degree : ").upper()
        while not all(x.isalpha() or x == "" or x == " " or x == "." for x in degree):
            print("Invalid format. Please enter valid degree.")
            degree = input("Enter degree : ")

        major = input("Enter major : ").upper()
        while not all(x.isalpha() or x == "" or x == " " for x in major):
            print("Invalid format. Please enter valid major.")
            major = input("Enter major : ")

        degreeID = degreeInfo(typeGraduation, degree, major)

        universityName = input("Name of University : ").upper()
        while not all(x.isalpha() or x == "" or x == " " for x in universityName):
            print("Invalid format. Please enter valid university name.")
            universityName = input("Name of University : ").upper()

        gpa = float(input("Enter GPA between 0 and 10 : "))
        while not(0.0 <= gpa <= 10.0):
            print("Invalid format. Please enter valid GPA.")
            gpa = float(input("Enter GPA between 0 and 10 : "))

        cur.execute("INSERT INTO HIGHER_EDUCATION VALUES (?, ?, ?, ?)", (memberID, degreeID, gpa, universityName))

        ch = input("If you have finished entering higher education information, please enter 0 : ")
        if int(ch) == 0:
            f = 0
        
    connection.commit()
    cur.close()

def skills(memberID):
    cur = connection.cursor()

    f = 1
    while f == 1:
        skill = input("Enter skill : ")
        while not all(x.isalpha() or x == "" or x == " " for x in skill):
                print("Invalid format. Please enter valid skill.")
                skill = input("Enter skill : ")

        experienceLevel = int(input("Enter experience level between 0 and 10 : "))
        while not(0 <= experienceLevel <= 10):
            print("Invalid format. Please enter valid experience level.")
            experienceLevel = int(input("Enter experience level between 0 and 10 : "))

        cur.execute("INSERT INTO SKILLS VALUES (?, ?, ?)", (memberID, skill, experienceLevel))

        ch = input("If you have finished entering your skills, please enter 0 : ")
        if int(ch) == 0:
            f = 0
    
    connection.commit()
    cur.close()
    
def projects(memberID):
    cur = connection.cursor()

    f = 1
    while f == 1:
        projectTitle = input("Enter project title : ")
        while not all(x.isalnum() or x == "" or x == " " for x in projectTitle):
                print("Invalid format. Please enter valid project title.")
                projectTitle = input("Enter project title : ")

        projDescription = input("Enter project description : ")
        while not all(x.isalnum() or x == "" or x == " " for x in projDescription):
                print("Invalid format. Please enter valid project description.")
                projDescription = input("Enter project description : ")

        cur.execute("INSERT INTO PROJECTS VALUES (?, ?, ?)", (memberID, projectTitle, projDescription))

        ch = input("If you have finished entering your projects, please enter 0 : ")
        if int(ch) == 0:
            f = 0

    connection.commit()
    cur.close()

def job(jobTitle, jobLocation, jobDescription, employer):
    cur = connection.cursor()

    checkJob = cur.execute("SELECT TITLE FROM JOB WHERE TITLE = ? AND LOCATION = ? AND DESCRIPTION = ? AND EMPLOYER = ?", (jobTitle, jobLocation, jobDescription, employer)).fetchall()
    if checkJob == []:
            jobList = cur.execute("SELECT JOB_ID FROM JOB").fetchall()
            if jobList == []:
                jobCount = 1
            else:
                jList = [i[0] for i in jobList]
                jobCount = int(max(jList)[4:10]) + 1
            jobID = "JOB#" + str(jobCount).zfill(6)
            cur.execute("INSERT INTO JOB VALUES (?, ?, ?, ?, ?)", (jobID, jobTitle, jobLocation, jobDescription, employer))
    else:
            jobID = cur.execute("SELECT JOB_ID FROM JOB WHERE TITLE = ? AND LOCATION = ? AND DESCRIPTION = ? AND EMPLOYER = ?", (jobTitle, jobLocation, jobDescription, employer)).fetchall[0][0]
    
    connection.commit()
    cur.close()

    return jobID

def experience(memberID):
    cur = connection.cursor()

    f = 1
    while f == 1:
        jobTitle = input("Enter job title : ")
        while not all(x.isalnum() or x == "" or x == " " for x in jobTitle):
            print("Invalid format. Please enter valid job title.")
            jobTitle = input("Enter job title : ")

        jobLocation = input("Enter job location : ")
        while not all(x.isalnum() or x == "" or x == " " for x in jobLocation):
            print("Invalid format. Please enter valid job location.")
            jobLocation = input("Enter job location : ")

        jobDescription = input("Enter job description : ")
        while not all(x.isalnum() or x == "" or x == " " for x in jobDescription):
            print("Invalid format. Please enter valid job description.")
            jobDescription = input("Enter job description : ")

        employer = input("Enter employer : ")
        while not all(x.isalpha() or x == "" or x == " " for x in employer):
            print("Invalid format. Please enter valid employer.")
            employer = input("Enter employer : ")

        jobID = job(jobTitle, jobLocation, jobDescription, employer)

        startDate = input('Enter start date (YYYY - MM - DD) : ')
        year, month, day = map(int, startDate.split('-'))
        startDate = date(year, month, day)

        endDate = input('Enter end date if applicable (YYYY - MM - DD), else enter NA : ').upper()
        if endDate != 'NA':
            year, month, day = map(int, endDate.split('-'))
            endDate = date(year, month, day)
            jobDuration = round((endDate - startDate).days / 365, 2)
        else:
            today = date.today()
            endDate = None
            jobDuration = round((today - startDate).days / 365, 2)
            
        startDate = startDate.strftime('%Y-%m-%d')

        cur.execute("INSERT INTO EXPERIENCE VALUES (?, ?, ?, ?, ?)", (memberID, jobID, startDate, endDate, jobDuration))
        
        ch = input("If you have finished entering your job details, please enter 0 : ")
        if int(ch) == 0:
            f = 0

    connection.commit()
    cur.close()

def accomplishments(memberID):
    cur = connection.cursor()

    f = 1
    while f == 1:
        accomplishment = input("Enter accomplishment : ")
        while not all(x.isalnum() or x == "" or x == " " for x in accomplishment):
                print("Invalid format. Please enter valid accomplishment.")
                accomplishment = input("Enter accomplishment : ")

        accDescription = input("Enter accomplishment description : ")
        while not all(x.isalnum() or x == "" or x == " " for x in accDescription):
                print("Invalid format. Please enter valid accomplishment description.")
                accDescription = input("Enter accomplishment description : ")

        cur.execute("INSERT INTO ACCOMPLISHMENTS VALUES (?, ?, ?)", (memberID, accomplishment, accDescription))

        ch = input("If you have finished entering your accomplishments, please enter 0 : ")
        if int(ch) == 0:
            f = 0

    connection.commit()
    cur.close()

def certifications(memberID):
    cur = connection.cursor()

    f = 1
    while f == 1:
        certificationURL = input("Enter certification URL as issued by the issuing authority : ")
        while not all(x.isalnum() or x == "" or x == " " for x in certificationURL):
                print("Invalid format. Please enter a valid certification URL.")
                certification = input("Enter certification URL as issued by the issuing authority : ")

        certification = input("Enter certification name : ")
        while not all(x.isalnum() or x == "" or x == " " for x in certification):
                print("Invalid format. Please enter valid certification.")
                certification = input("Enter certification : ")

        cur.execute("INSERT INTO CERTIFICATIONS VALUES (?, ?, ?)", (memberID, certificationURL, certification))

        ch = input("If you have finished entering your certifications, please enter 0 : ")
        if int(ch) == 0:
            f = 0

    connection.commit()
    cur.close()

def queryResults(memberID):
    cur = connection.cursor()

    bDetails = cur.execute("SELECT M.NAME, M.BIO, M.ADDRESS, M.PHONE, M.EMAIL, M.GITHUB, M.LINKEDIN FROM MEMBER M WHERE M.MEMBER_ID = ?", memberID).fetchall()
    sDetails = cur.execute("SELECT S.NAME AS SCHOOL, S.LOCATION, SCH.PASSING_LEVEL, SCH.PASSING_YEAR, SCH.STREAM, SCH.SCORE FROM MEMBER M INNER JOIN SCHOOLING SCH ON M.MEMBER_ID = SCH.MEMBER_ID INNER JOIN SCHOOL S ON SCH.SCHOOL_ID = S.SCHOOL_ID WHERE M.MEMBER_ID = ?", memberID).fetchall()
    hDetails = cur.execute("SELECT D.DEGREE, D.MAJOR, H.UNIVERSITY, H.GPA FROM MEMBER M INNER JOIN HIGHER_EDUCATION H ON M.MEMBER_ID = H.MEMBER_ID INNER JOIN DEGREE_INFO D ON H.DEGREE_ID = D.DEGREE_ID WHERE M.MEMBER_ID = ?", memberID).fetchall()
    jDetails = cur.execute("SELECT J.EMPLOYER, J.LOCATION, J.TITLE, J.DESCRIPTION, E.DURATION FROM MEMBER M INNER JOIN EXPERIENCE E ON M.MEMBER_ID = E.MEMBER_ID INNER JOIN JOB J ON E.JOB_ID = J.JOB_ID WHERE M.MEMBER_ID = ?", memberID).fetchall()
    pDetails = cur.execute("SELECT P.PROJECT_NAME, P.DESCRIPTION FROM MEMBER M INNER JOIN PROJECTS P ON M.MEMBER_ID = P.MEMBER_ID WHERE M.MEMBER_ID = ?", memberID).fetchall()
    skDetails = cur.execute("SELECT SK.SKILL_NAME, SK.EXPERIENCE_LEVEL FROM MEMBER M INNER JOIN SKILLS SK ON M.MEMBER_ID = SK.MEMBER_ID WHERE M.MEMBER_ID = ?", memberID).fetchall()
    aDetails = cur.execute("SELECT A.ACCOMPLISHMENT_NAME, A.DESCRIPTION FROM MEMBER M INNER JOIN ACCOMPLISHMENTS A ON M.MEMBER_ID = A.MEMBER_ID WHERE M.MEMBER_ID = ?", memberID).fetchall()
    cDetails = cur.execute("SELECT C.CERTIFICATION_URL, C.CERTIFICATE_NAME FROM MEMBER M INNER JOIN CERTIFICATIONS C ON M.MEMBER_ID = C.MEMBER_ID WHERE M.MEMBER_ID = ?", memberID).fetchall()
    connection.commit()
    cur.close()

    return [bDetails, sDetails, hDetails, jDetails, pDetails, skDetails, aDetails, cDetails]

def displayDetails(memberID):
    bDetails, sDetails, hDetails, jDetails, pDetails, skDetails, aDetails, cDetails = queryResults(memberID)
    print("Basic details : ", bDetails)
    print("Schooling details : ", sDetails)
    print("Higher education details : ", hDetails)
    print("Job details : ", jDetails)
    print("Project details : ", pDetails)
    print("Skills details : ", skDetails)
    print("Accomplishments details : ", aDetails)
    print("Certifiction details : ", cDetails)

def clientInfo(memberID):
    bDetails, sDetails, hDetails, jDetails, pDetails, skDetails, aDetails, cDetails = queryResults(memberID)
    name, bio, address, phone, email, github, linkedin = bDetails[0][0], bDetails[0][1], bDetails[0][2], bDetails[0][3], bDetails[0][4], bDetails[0][5], bDetails[0][6]
    return {"name" : name, "bio" : bio, "address" : address, "phone" : phone, "email" : email, "web_info": github+'\n'+linkedin, "schooling" : sDetails, "higherEducation" : hDetails, "jobs" : jDetails, "projects" : pDetails, "skills" : skDetails, "accomplishments" : aDetails, "certifications" : cDetails}
    
def registerAccount():
    memberID = createMember()
    schooling(memberID)
    higherEducation(memberID)
    skills(memberID)
    projects(memberID)
    experience(memberID)
    accomplishments(memberID)
    certifications(memberID)
    return memberID

def structureDetails(items):
    schooling = ""
    higher_ed = ""
    experience = ""
    experience = ""
    projects = ""
    skills = ""
    accomplishments = ""
    certifications = ""

    school_format = "{}, {}\n{}th Board Examinations {}\n{}, Percentage: {}%\n\n"
    higher_ed_format = "{}\n{} {}\nCGPA: {}\n\n"
    exp_format = "{} - {}, {}\n{} - {} years\n\n"
    project_format = "{}\n{}\n\n"
    skill_format = "{}\n"
    accomplish_format = "{}\n{}\n\n"
    certification_format = "{}\n{}\n\n"


    for i in items["schooling"][::-1]:
        schooling += school_format.format(*i)
    schooling = schooling.strip()

    for i in items["higherEducation"][::-1]:
        higher_ed += higher_ed_format.format(i[2], i[0], i[1], i[3])
    higher_ed = higher_ed.strip()

    for i in items["jobs"][::-1]:
        experience += exp_format.format(i[2], i[0], i[1], i[3], i[4])
    experience = experience.strip()

    for i in items["projects"]:
        projects += project_format.format(*i)
    projects = projects.strip()

    for i in items["skills"]:
        skills += skill_format.format(i[0])
    skills = skills.strip()

    for i in items["accomplishments"][::-1]:
        accomplishments += accomplish_format.format(*i)
    accomplishments = accomplishments.strip()

    for i in items["certifications"][::-1]:
        certifications += certification_format.format(*i)
    certifications = certifications.strip()

    resume_values = {"name" : items["name"],
        "bio" : items["bio"],
        "address" : items["address"],
        "phone" : items["phone"],
        "email" : items["email"],
        "experience" : experience,
        "websites" : items["web_info"],
        "education" : higher_ed + '\n\n' + schooling,
        "projects" : projects,
        "skills" : skills,
        "certifications" : certifications,
        "accomplishments" : accomplishments}

    return resume_values