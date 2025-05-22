"""Command Line Interface (to get database)"""

from src.classes import Course, Student
from constants.variables import conn
import src.DB_commands as db_commands


class Interface:
	def __init__(self):
		self.current_student = None
		self.login_text = ["Login", "Create User", "Exit"]

		self.main_text = ["View Course Settings", "View Programs", "Filters", "View Courses Selected", "Exit"]
		self.main_func = [self.manage_courses, self.manage_programs, self.manage_filters, self.view_selected_courses]

		self.all_courses_text = ["Add Course", "Remove Course", "View All Courses", "Exit"]
		self.all_courses_func = [self.add_course, self.remove_course, self.view_all_courses]

		self.all_programs_text = ["Add Program", "Remove Program", "View All Programs", "Exit"]
		self.all_programs_func = [self.add_program, self.remove_program, self.view_all_programs]

		self.filters_text = ["Filter By Course Subjects", "Filter By Course Points", "Reset Filters", "Exit"]
		self.filters_func = [self.filter_subjects, self.filter_points, self.filter_reset]

	def checkInput(self, temp):
		result = True
		try:
			temp = int(temp)
		except Exception:
			print("Input a number for command usage.")
			result = False

		if temp >= len(self.main_text):
			print("Input number out of range (not an available command.)")
			result = False
		return result

	def command_print(self, current_text):
		print("\nAvailable commands: ")
		for index, text in enumerate(current_text):
			print(f"\t{index}. {text}")

	# reminder: login is only checking for a user now, need to associate "Selected courses" with specific login (and only show for that user)
	def login(self):
		students: list["Student"] = db_commands.get_students()
		while True:
			self.command_print(self.login_text)
			user_input = input("Input command: ")
			if self.checkInput(user_input):
				students = []
				if self.login_text[int(user_input) == "Exit"]:
					break

				username = input("Input Username:")

				if int(user_input) == 1:  # login
					for student in students:
						if student.Name == username:
							self.main_interface()
					if students == []:
						print("User login not found.")

				elif int(user_input) == 2:  # Create user
					for student in students:
						if student.Name == username:
							print("Username already in use.")
							continue
					db_commands.create_student(username)

	def main_interface(self):
		while True:
			self.command_print(self.main_text)

			command = input("Input given: ")

			if not self.checkInput(command):
				continue
			if self.main_text[command] == "Exit":  # exit
				break

			for index, _ in enumerate(self.main_text):
				if command == index:
					self.main_func[index]()
					continue

	def manage_courses(self):
		while True:
			self.command_print(self.all_courses_text)

			command = input("Input given: ")

			if not self.checkInput(command):
				continue
			if self.all_courses_text[command] == "Exit":  # exit
				break

			for index, _ in enumerate(self.all_courses_text):
				if command == index:
					self.all_courses_func[index]()
					continue

	def manage_programs(self):
		while True:
			self.command_print(self.all_programs_text)

			command = input("Input given: ")

			if not self.checkInput(command):
				continue
			if self.all_programs_text[command] == "Exit":  # exit
				break

			for index, _ in enumerate(self.all_programs_text):
				if command == index:
					self.all_programs_func[index]()
					continue

	def manage_filters(self):
		while True:
			self.command_print(self.filters_text)

			command = input("Input given: ")

			if not self.checkInput(command):
				continue
			if self.filters_text[command] == "Exit":  # exit
				break

			for index, _ in enumerate(self.filters_text):
				if command == index:
					self.filters_func[index]()
					continue

	def view_selected_courses(self):
		pass

	def add_course(self):
		pass

	def remove_course(self):
		pass

	def view_all_courses(self):
		pass

	def add_program(self):
		pass

	def remove_program(self):
		pass

	def view_all_programs(self):
		pass

	def filter_subjects(self):
		pass

	def filter_points(self):
		pass

	def filter_reset(self):
		pass

	def courses_selected_view(self):
		# program chosen: program_2 || [NO CHOSEN PROGRAM]
		# Courses \nMa1448 [ECST, Subjects]\n, ...
		cursor = self.conn.cursor()

		cursor.execute(
			"SELECT * FROM ´StudentEnrollment´ WHERE StudentID = %s",
		)
		return_value = cursor.fetchall()


def main():
	interface = Interface()
	interface.start_interface()


if __name__ == "__main__":
	main()
