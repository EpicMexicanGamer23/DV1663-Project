from getpass import getpass

import mysql.connector as mysql
import src.gen as gen
from src.classes import Course
from src.CLI import Interface

conn : mysql.MySQLConnection = None
username : str
mysqlpassword = None

def init_database():
	global conn
	global mysqlpassword
	global username
	cursor = conn.cursor()
	cursor.execute("CREATE DATABASE IF NOT EXISTS `dv1663_group_12`")
	cursor.close()
	conn.close()
	conn = mysql.connect(host="localhost", user = username, password=mysqlpassword, database = "dv1663_group_12")
	conn.commit()

def init_tables():
	global conn
	cursor = conn.cursor()
	
	table_courses = """CREATE TABLE IF NOT EXISTS `Courses` (
		CourseID VARCHAR(10) NOT NULL,
		ETCSCredits INT NOT NULL,
		EducationLevel VARCHAR(20) NOT NULL,
		StudyPeriod INT NOT NULL,
		TeachingLanguage VARCHAR(100) NOT NULL,

		PRIMARY KEY (CourseID)
	);
	"""
	
	table_courses_required = """CREATE TABLE IF NOT EXISTS `CoursesRequired`(
		CourseID VARCHAR(10) NOT NULL,
		RequirementCourse VARCHAR(10) NOT NULL,
		
		FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
		FOREIGN KEY (RequirementCourse) REFERENCES Courses(CourseID),
		PRIMARY KEY (CourseID, RequirementCourse)
	);
	"""

	table_courses_subject = """CREATE TABLE IF NOT EXISTS `CourseSubject`(
		CourseID VARCHAR(10) NOT NULL,
		Subject VARCHAR(100) NOT NULL,

		FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
		PRIMARY KEY (CourseID, Subject)
	);
	"""
	
	table_subject_requirements = """CREATE TABLE IF NOT EXISTS `SubjectRequirements`(
		CourseID VARCHAR(10) NOT NULL,
		Subject VARCHAR(100) NOT NULL,
		Credits INT NOT NULL,

		FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
		PRIMARY KEY (CourseID, Subject)
	);
	"""

	table_programs = """CREATE TABLE IF NOT EXISTS `Programs`(
		ProgramID INT NOT NULL,
		ProgramCredits INT NOT NULL,

		PRIMARY KEY (ProgramID)
	);
	"""

	table_program_courses = """CREATE TABLE IF NOT EXISTS `ProgramCourses` (
		ProgramID INT NOT NULL,
		CourseID VARCHAR(10) NOT NULL,

		FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
		FOREIGN KEY (ProgramID) REFERENCES Programs(ProgramID),
		PRIMARY KEY (CourseID, ProgramID)
	);
	"""

	table_students = """CREATE TABLE IF NOT EXISTS `Students` (
		StudentID INT NOT NULL,
		Name VARCHAR(100) NOT NULL,
		ProgramID INT NOT NULL,

		FOREIGN KEY (ProgramID) REFERENCES Programs(ProgramID),
		PRIMARY KEY (StudentID)
	);
	"""

	table_student_enrollment = """
	CREATE TABLE IF NOT EXISTS `StudentEnrollment` (
		CourseID VARCHAR(10) NOT NULL,
		StudentID INT NOT NULL,
		StudentCredits INT NOT NULL,
		CourseCredits INT NOT NULL,

		FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
		FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
		PRIMARY KEY (CourseID, StudentID)
	);
	"""

	cursor.execute(table_courses)
	cursor.execute(table_courses_required)
	cursor.execute(table_courses_subject)
	cursor.execute(table_subject_requirements)
	cursor.execute(table_programs)
	cursor.execute(table_program_courses)
	cursor.execute(table_students)
	cursor.execute(table_student_enrollment)
	conn.commit()
	cursor.close()

def drop_tables():
	global conn
	cursor = conn.cursor()
	cursor.execute("DROP TABLE IF EXISTS `CoursesRequired`;")
	cursor.execute("DROP TABLE IF EXISTS `CourseSubject`;")
	cursor.execute("DROP TABLE IF EXISTS `SubjectRequirements`;")
	cursor.execute("DROP TABLE IF EXISTS `ProgramCourses`;")
	cursor.execute("DROP TABLE IF EXISTS `StudentEnrollment`;")
	cursor.execute("DROP TABLE IF EXISTS `Courses`;")
	cursor.execute("DROP TABLE IF EXISTS `Students`;")
	cursor.execute("DROP TABLE IF EXISTS `Programs`;")
	conn.commit()
	cursor.close()
	print("DROPPED ALL TABLES")

def fill_course_table():
	global conn
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM Courses")
	query = cursor.fetchall()
	if(len(query) != 0):
		return
	generated_coures : list["Course"] = gen.generate_100_courses()
	for course in generated_coures:
		data = course.get_values()
		cursor.execute("INSERT INTO Courses(CourseID, ETCSCredits, EducationLevel, StudyPeriod, TeachingLanguage) VALUES(%s, %s, %s, %s, %s)",data)
		subjects = course.get_subjects()
		for subject in subjects:
			sub_data = (data[0], subject[0])
			cursor.execute("INSERT INTO CourseSubject(CourseID, Subject) VALUES(%s, %s)", sub_data)
		req_courses : list["Course"] = course.get_requirement_courses()
		for req_course in req_courses:
			req_data = (data[0], req_course.id)
			cursor.execute("INSERT INTO CoursesRequired(CourseID, RequirementCourse) VALUES(%s, %s)", req_data)
	conn.commit()	#have to commit to save added value in table
	cursor.close()
	return

def main():
	global conn
	global username
	global mysqlpassword
	connected = False
	while(not connected):
		username = input("MYSQL Server User: ")
		mysqlpassword = getpass("MYSQL Server Password: ")
		try:
			conn = mysql.connect(host="localhost", user = username, password=mysqlpassword )
		except Exception:
			print("Connection failed, make sure the MYSQL Server is active, and the password is correct")
			continue
		if(conn.is_connected()):
			connected = True

	print("CONNECTED")
	init_database()
	init_tables()
	fill_course_table()
	interface = Interface()
	interface.login()
	conn.close()

if __name__ == "__main__":
	main()
