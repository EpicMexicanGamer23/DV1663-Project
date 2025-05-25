import constants.variables as cvars
import mysql.connector as mysql
from src.classes import Student, Course, Program


def get_students() -> list["Student"]:
	cursor = cvars.conn.cursor()
	cursor.execute("SELECT * FROM Students")
	students = cursor.fetchall()
	cursor.close()
	student_list = []
	for element in students:
		student_list.append(Student(element))
	return student_list


def get_student(student_id: int) -> "Student":
	cursor = cvars.conn.cursor()
	cursor.execute("SELECT * FROM Students WHERE StudentID = %s", (student_id,))
	student_data = cursor.fetchall()
	cursor.close()
	return Student(student_data[0])


def create_student(username: str):
	cursor = cvars.conn.cursor()
	username = username.lower()
	cursor.execute("INSERT INTO Students(Name) VALUES(%s)", (username,))
	cvars.conn.commit()
	cursor.close()
	return


def get_courses(student_id):
	cursor = cvars.conn.cursor()
	cursor.execute(
		"""SELECT c.*, vcs.Subjects, vcr.Requirements,
			CASE WHEN se.StudentID IS NOT NULL THEN 1 ELSE 0 END AS IsStudentEnrolled
			FROM courses c
			LEFT JOIN view_course_subjects vcs ON c.CourseID = vcs.CourseID
			LEFT JOIN view_course_requirements vcr ON c.CourseID = vcr.CourseID
			LEFT JOIN studentenrollment se ON c.CourseID = se.CourseID AND se.StudentID = %s
			ORDER BY 
	IsStudentEnrolled DESC, 
    c.CourseID;""",
		(student_id,),
	)
	courses = cursor.fetchall()
	cursor.close()
	course_list = []
	for element in courses:
		course_list.append(Course(element[0], element[1], element[2], element[3], element[4], element[5], element[6]))
	return course_list


def get_student_enrollment(student_ID):
	cursor = cvars.conn.cursor()
	cursor.execute(
		"""SELECT se.* FROM studentenrollment se 
			WHERE se.studentID = "%s";""",
		(student_ID,),
	)
	courses = cursor.fetchall()
	cursor.close()
	course_list = []
	for element in courses:
		course_list.append(element[0])
	return course_list


def get_programs():
	cursor = cvars.conn.cursor()
	cursor.execute("SELECT * FROM Programs")
	programs = cursor.fetchall()
	program_list = []
	for program in programs:
		program_list.append(Program(program))
	cursor.close()
	return program_list


def get_program_courses(programs: list[int]) -> list[str]:
	cursor = cvars.conn.cursor()
	courses = []
	for program in programs:
		cursor.execute("SELECT * FROM ProgramCourses WHERE ProgramID = %s", (program,))
		courses += cursor.fetchall()
	course_list = []
	for course in courses:
		course_list.append(course[1])
	cursor.close()
	return course_list


def add_to_student_enrollment(studentID, courseID):
	cursor = cvars.conn.cursor()
	cursor.execute(
		"""INSERT INTO studentenrollment(CourseID, studentID) VALUES(%s, %s)""",
		(courseID, studentID),
	)
	cursor.callproc("req_insert_courses", (courseID, studentID))
	cvars.conn.commit()
	cursor.close()


def remove_from_student_enrollment(student_id, course_id):
	cursor = cvars.conn.cursor()
	cursor.execute(
		"""DELETE FROM studentenrollment WHERE CourseID = %s AND studentID = %s;""",
		(course_id, student_id),
	)
	cvars.conn.commit()
	cursor.close()


def set_student_program(programID, studentID):
	cursor = cvars.conn.cursor()
	cursor.execute("UPDATE Students SET ProgramID = %s WHERE StudentID = %s", (programID, studentID))
	cursor.close()
	cvars.conn.commit()
