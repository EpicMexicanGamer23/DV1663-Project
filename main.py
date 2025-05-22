from getpass import getpass

import mysql.connector as mysql
import src.gen as gen
from src.classes import Course, Program
from src.CLI import Interface

import constants.variables as vars


def init_database():
	cursor = vars.conn.cursor()
	cursor.execute("CREATE DATABASE IF NOT EXISTS dv1663_group_12")
	cursor.close()
	vars.conn.close()
	vars.conn = mysql.connect(host="localhost", user=vars.username, password=vars.mysqlpassword, database="dv1663_group_12")
	vars.conn.commit()


def init_tables():
	cursor = vars.conn.cursor()

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
		StudentID INT NOT NULL AUTO_INCREMENT,
		Name VARCHAR(100) NOT NULL,
		ProgramID INT,

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
	vars.conn.commit()
	cursor.close()


def drop_tables():
	cursor = vars.conn.cursor()
	cursor.execute("DROP TABLE IF EXISTS `CoursesRequired`;")
	cursor.execute("DROP TABLE IF EXISTS `CourseSubject`;")
	cursor.execute("DROP TABLE IF EXISTS `SubjectRequirements`;")
	cursor.execute("DROP TABLE IF EXISTS `ProgramCourses`;")
	cursor.execute("DROP TABLE IF EXISTS `StudentEnrollment`;")
	cursor.execute("DROP TABLE IF EXISTS `Courses`;")
	cursor.execute("DROP TABLE IF EXISTS `Students`;")
	cursor.execute("DROP TABLE IF EXISTS `Programs`;")
	vars.conn.commit()
	cursor.close()
	print("DROPPED ALL TABLES")


def insert_course(course: "Course"):
	cursor = vars.conn.cursor()
	# Insert the course information into the Course Table
	data = course.get_values()
	cursor.execute("INSERT INTO Courses(CourseID, ETCSCredits, EducationLevel, StudyPeriod, TeachingLanguage) VALUES(%s, %s, %s, %s, %s)", data)
	# Inser the subjects for the course in the CourseSubject Table
	subjects = course.get_subjects()
	for subject in subjects:
		sub_data = (data[0], subject[0])
		cursor.execute("INSERT INTO CourseSubject(CourseID, Subject) VALUES(%s, %s)", sub_data)
	# Inser the requirement courses into the CoursesRequired Table
	req_courses: list["Course"] = course.get_requirement_courses()
	for req_course in req_courses:
		req_data = (data[0], req_course.id)
		cursor.execute("INSERT INTO CoursesRequired(CourseID, RequirementCourse) VALUES(%s, %s)", req_data)

	vars.conn.commit()
	cursor.close()


def insert_program(program: "Program"):
	cursor = vars.conn.cursor()
	# Insert the program information into the Program Table
	cursor.execute("INSERT INTO Programs(ProgramID, ProgramCredits) VALUES(%s,%s)", program.get_values())
	courses = program.get_courses()
	for course in courses:
		data = (program.id, course.id)
		insert_course(course)  # Inser the course into the Course Table
		# Insert the course into the ProgramCourses Table
		cursor.execute("INSERT INTO ProgramCourses(ProgramID, CourseID) VALUES(%s, %s)", data)

	vars.conn.commit()
	cursor.close()


def fill_course_table():
	cursor = vars.conn.cursor()
	cursor.execute("SELECT * FROM Courses")
	query = cursor.fetchall()
	if len(query) != 0:
		cursor.close()
		return
	generated_coures: list["Course"] = gen.generate_100_courses()
	for course in generated_coures:
		insert_course(course)
	vars.conn.commit()
	cursor.close()
	return


def fill_program_table(program_amount: int):
	cursor = vars.conn.cursor()
	cursor.execute("SELECT * FROM Programs")
	query = cursor.fetchall()
	if len(query) != 0:
		cursor.close()
		return
	for _ in range(program_amount):
		prog: "Program" = gen.generate_program()
		insert_program(prog)
	vars.conn.commit()
	cursor.close()
	return


def main():
	connected = False
	while not connected:
		vars.username = input("MYSQL Server User: ")
		vars.mysqlpassword = getpass("MYSQL Server Password: ")

		try:
			vars.conn = mysql.connect(host="localhost", user=vars.username, password=vars.mysqlpassword)
		except Exception:
			print("Connection failed, make sure the MYSQL Server is active, and the password is correct")
			continue
		if vars.conn.is_connected():
			connected = True

	print("CONNECTED")
	init_database()
	init_tables()
	# drop_tables()
	# fill_course_table()
	# fill_program_table(4)
	interface = Interface()
	interface.login()
	vars.conn.close()


if __name__ == "__main__":
	main()
