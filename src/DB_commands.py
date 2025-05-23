import constants.variables as vars
import mysql.connector as mysql
from src.classes import Student, Course, Program


def get_students() -> list["Student"]:
	cursor = vars.conn.cursor()
	cursor.execute("SELECT * FROM Students")
	students = cursor.fetchall()
	cursor.close()
	student_list = []
	for element in students:
		student_list.append(Student(element))
	return student_list


def get_student(student_id: int) -> "Student":
	cursor = vars.conn.cursor()
	cursor.execute("SELECT * FROM Students WHERE StudentID = %s", (student_id,))
	student_data = cursor.fetchall()
	cursor.close()
	return Student(student_data[0])


def create_student(username: str):
	cursor = vars.conn.cursor()
	username = username.lower()
	cursor.execute("INSERT INTO Students(Name) VALUES(%s)", (username,))
	vars.conn.commit()
	cursor.close()
	return


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


def get_programs():
	cursor = vars.conn.cursor()
	cursor.execute("SELECT * FROM Programs")
	programs = cursor.fetchall()
	program_list = []
	for program in programs:
		program_list.append(Program(program))
	cursor.close()
	return program_list
