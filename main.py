from getpass import getpass

import mysql.connector as mysql
import src.gen as gen
from src.classes import Course, Program
from src.CLI import Interface

import constants.variables as cvars


def init_database():
	cursor = cvars.conn.cursor()
	cursor.execute("CREATE DATABASE IF NOT EXISTS dv1663_group_12")
	cvars.conn.commit()
	cursor.close()
	cvars.conn.close()
	cvars.conn = mysql.connect(host="localhost", user=cvars.username, password=cvars.mysqlpassword, database="dv1663_group_12")


def init_views():
	cursor = cvars.conn.cursor()

	course_subjects = """CREATE OR REPLACE VIEW view_course_subjects AS
	SELECT 
		CourseID, 
		GROUP_CONCAT(Subject SEPARATOR ', ') AS Subjects
		FROM 
			CourseSubject
		GROUP BY 
			CourseID;"""

	course_requirements = """CREATE OR REPLACE VIEW view_course_requirements AS
	SELECT
		CourseID,
		GROUP_CONCAT(RequirementCourse SEPARATOR ', ') AS Requirements
		FROM
			coursesrequired
		GROUP BY
			CourseID;"""
	cursor.execute(course_subjects)
	cursor.execute(course_requirements)
	cvars.conn.commit()
	cursor.close()


def init_tables():
	cursor = cvars.conn.cursor()

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

	table_student_enrollment = """CREATE TABLE IF NOT EXISTS `StudentEnrollment` (
		CourseID VARCHAR(10) NOT NULL,
		StudentID INT NOT NULL,

		FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
		FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
		PRIMARY KEY (CourseID, StudentID)
	);
	"""

	cursor.execute(table_courses)
	cursor.execute(table_courses_required)
	cursor.execute(table_courses_subject)
	cursor.execute(table_programs)
	cursor.execute(table_program_courses)
	cursor.execute(table_students)
	cursor.execute(table_student_enrollment)
	cvars.conn.commit()
	cursor.close()


def init_func_procedures():
	remove_program_courses = """
	DELIMITER $$
	CREATE PROCEDURE remove_program_courses(IN program_id INT, IN student_id INT)
	BEGIN
		DELETE FROM StudentEnrollment
			WHERE StudentEnrollment.CourseID IN (
				SELECT CourseID FROM ProgramCourses WHERE ProgramCourses.ProgramID = program_id
				) 
				AND StudentEnrollment.StudentID = student_id;
	END $$
	DELIMITER ;
	"""
	add_program_courses = """
	DELIMITER $$
	CREATE PROCEDURE add_program_courses (IN program_id INT, IN student_id INT)
	BEGIN
		INSERT INTO StudentEnrollment(CourseID, StudentID)
			SELECT CourseID, student_id
			FROM ProgramCourses
			WHERE ProgramCourses.ProgramID = program_id;
	END $$
	DELIMITER ;
	"""

	cursor = cvars.conn.cursor()
	cursor.execute("DROP PROCEDURE IF EXISTS add_program_courses")
	cursor.execute(add_program_courses)
	cursor.execute("DROP PROCEDURE IF EXISTS remove_program_courses")
	cursor.execute(remove_program_courses)
	cursor.close()
	cvars.conn.commit()
	return


def init_triggers():
	program_update_remove_trigger = """
	DELIMITER $$
	CREATE TRIGGER remove_program_trigger
	BEFORE UPDATE
	ON Students
	FOR EACH ROW
	BEGIN
		IF OLD.ProgramID IS NOT NULL THEN
			IF NEW.ProgramID IS NOT NULL THEN
				IF OLD.ProgramID <> NEW.ProgramID THEN
					CALL remove_program_courses(OLD.ProgramID, OLD.StudentID);
				END IF;
			ELSE
				CALL remove_program_courses(OLD.ProgramID, OLD.StudentID);
			END IF;
		END IF;
	END$$
	DELIMITER ;
	"""

	program_update_add_trigger = """
	DELIMITER $$
	CREATE TRIGGER add_program_trigger
	AFTER UPDATE
	ON Students
	FOR EACH ROW
	BEGIN
		IF NEW.ProgramID IS NOT NULL THEN
			IF OLD.ProgramID IS NULL THEN
				CALL add_program_courses(NEW.ProgramID, NEW.StudentID);
			ELSE
				IF OLD.ProgramID <> NEW.ProgramID THEN
					CALL add_program_courses(NEW.ProgramID, NEW.StudentID);
				END IF;
			END IF;
		END IF;
	END$$
	DELIMITER ;
"""
	cursor = cvars.conn.cursor()
	cursor.execute("DROP TRIGGER IF EXISTS add_program_trigger")
	cursor.execute(program_update_add_trigger)
	cursor.execute("DROP TRIGGER IF EXISTS remove_program_trigger")
	cursor.execute(program_update_remove_trigger)
	cursor.close()
	cvars.conn.commit()


def drop_tables():
	cursor = cvars.conn.cursor()
	cursor.execute("DROP TABLE IF EXISTS `CoursesRequired`;")
	cursor.execute("DROP TABLE IF EXISTS `CourseSubject`;")
	cursor.execute("DROP TABLE IF EXISTS `ProgramCourses`;")
	cursor.execute("DROP TABLE IF EXISTS `StudentEnrollment`;")
	cursor.execute("DROP TABLE IF EXISTS `Courses`;")
	cursor.execute("DROP TABLE IF EXISTS `Students`;")
	cursor.execute("DROP TABLE IF EXISTS `Programs`;")
	cvars.conn.commit()
	cursor.close()
	print("DROPPED ALL TABLES")


def insert_course(course: "Course"):
	cursor = cvars.conn.cursor()
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

	cvars.conn.commit()
	cursor.close()


def insert_program(program: "Program"):
	cursor = cvars.conn.cursor()
	# Insert the program information into the Program Table
	cursor.execute("INSERT INTO Programs(ProgramID, ProgramCredits) VALUES(%s,%s)", program.get_values())
	courses = program.get_courses()
	for course in courses:
		data = (program.id, course.id)
		insert_course(course)  # Inser the course into the Course Table
		# Insert the course into the ProgramCourses Table
		cursor.execute("INSERT INTO ProgramCourses(ProgramID, CourseID) VALUES(%s, %s)", data)

	cvars.conn.commit()
	cursor.close()


def fill_course_table():
	cursor = cvars.conn.cursor()
	cursor.execute("SELECT * FROM Courses")
	query = cursor.fetchall()
	if len(query) != 0:
		cursor.close()
		return
	generated_coures: list["Course"] = gen.generate_100_courses()
	for course in generated_coures:
		insert_course(course)
	cvars.conn.commit()
	cursor.close()
	return


def fill_program_table(program_amount: int):
	cursor = cvars.conn.cursor()
	cursor.execute("SELECT * FROM Programs")
	query = cursor.fetchall()
	if len(query) != 0:
		cursor.close()
		return
	for _ in range(program_amount):
		prog: "Program" = gen.generate_program()
		insert_program(prog)
	cvars.conn.commit()
	cursor.close()
	return


def main():
	connected = False
	while not connected:
		cvars.username = input("MYSQL Server User: ")
		cvars.mysqlpassword = getpass("MYSQL Server Password: ")

		try:
			cvars.conn = mysql.connect(host="localhost", user=cvars.username, password=cvars.mysqlpassword)
		except Exception:
			print("Connection failed, make sure the MYSQL Server is active, and the password is correct")
			continue
		if cvars.conn.is_connected():
			connected = True

	print("CONNECTED")
	init_database()
	init_tables()
	init_func_procedures()
	init_triggers()
	# drop_tables()
	fill_course_table()
	fill_program_table(4)
	interface = Interface()
	interface.login()
	cvars.conn.close()


if __name__ == "__main__":
	main()
