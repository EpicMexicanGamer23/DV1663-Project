import constants.variables as vars
import mysql.connector as mysql
from src.classes import Student


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


def get_student_enrollment():
	cursor = vars.conn.cursor()
