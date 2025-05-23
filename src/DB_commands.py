import constants.variables as vars
import mysql.connector as mysql
from src.classes import Student, Course


def get_students():
	cursor = vars.conn.cursor()
	cursor.execute("SELECT * FROM Students")
	students = cursor.fetchall()
	cursor.close()
	student_list = []
	for element in students:
		student_list.append(Student(element))
	return student_list


def create_student(username: str):
	cursor = vars.conn.cursor()
	username = username.lower()
	cursor.execute("INSERT INTO Students(Name) VALUES(%s)", (username,))
	vars.conn.commit()
	cursor.close()
	return


def get_courses(student_id):
	cursor = vars.conn.cursor()
	cursor.execute(
		"""SELECT c.*, vcs.Subjects, vcr.Requirements
	FROM courses c
		LEFT JOIN 
				view_course_subjects vcs ON c.CourseID = vcs.CourseID
		LEFT JOIN 
				view_course_requirements vcr ON c.CourseID = vcr.CourseID
		LEFT JOIN 
				studentenrollment se ON c.CourseID = se.CourseID AND se.StudentID = %s
ORDER BY 
	se.StudentID DESC;""",
		(student_id,),
	)
	courses = cursor.fetchall()
	cursor.close()
	course_list = []
	for element in courses:
		course_list.append(Course(element[0], element[1], element[2], element[3], element[4], element[5], element[6]))
	return course_list


def working_get_courses():
	cursor = vars.conn.cursor()

	cursor.execute("""SELECT c.*, vcs.Subjects, vcr.Requirements
		FROM courses c
		LEFT JOIN 
				view_course_subjects vcs 
				ON c.CourseID = vcs.CourseID
		LEFT JOIN 
				view_course_requirements vcr 
				ON c.CourseID = vcr.CourseID
		;""")
	courses = cursor.fetchall()
	cursor.close()
	course_list = []
	for element in courses:
		course_list.append(Course(element[0], element[1], element[2], element[3], element[4], element[5], element[6]))
	return course_list


def get_student_enrollment(student_ID):
	cursor = vars.conn.cursor()
	cursor.execute("""""")
	courses = cursor.fetchall()
	cursor.close()
	course_list = []
	for element in courses:
		course_list.append(Course(element[0], element[1], element[2], element[3], element[4], element[5], element[6]))
	return course_list


def add_course_to_student():
	cursor = vars.conn.cursor()
	cursor.execute("""""")
	vars.conn.commit()
	cursor.close()
	pass
