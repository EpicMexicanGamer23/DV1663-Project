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


def create_student(username):
	cursor = vars.conn.cursor()
	cursor.execute("INSERT INTO Students (Name) VALUES(%s)", username)


def get_student_enrollment(student_ID):
	# cursor = vars.conn.cursor()

	pass


def get_courses():
	cursor = vars.conn.cursor()
	cursor.execute("SELECT * FROM Courses")
	courses = cursor.fetchall()
	cursor.close()
	course_list = []
	for element in courses:
		course_list.append(Course(element))
	return course_list
