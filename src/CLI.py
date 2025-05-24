"""Command Line Interface (to get database)"""

from src.classes import Course, Student, Program
import constants.variables as cvars
import src.DB_commands as db_commands


class Interface:
	def __init__(self):
		self.current_student_id = None
		self.login_text = ["Login", "Create User", "Exit"]
		self.title_text = ["MENU", "COURSE MANAGEMENT", "PROGRAM MANAGEMENT", "FILTERS"]

		self.main_text = ["View Course Settings", "View Programs", "Filters", "View Selection", "Exit"]
		self.main_func = [self.manage_courses, self.manage_programs, self.manage_filters, self.view_selected_courses]

		self.all_courses_text = ["Add Course", "Remove Course", "View All Courses", "Exit"]

		self.all_courses_func = [self.add_course_to_student, self.remove_course_from_student, self.view_all_courses]

		self.all_programs_text = ["Add Program", "Remove Program", "View All Programs", "Exit"]
		self.all_programs_func = [self.add_program_to_student, self.remove_program_from_student, self.view_all_programs]

		self.filters_text = ["Filter By Course Subjects", "Filter By Course Points", "Reset Filters", "Exit"]
		self.filters_func = [self.filter_subjects, self.filter_points, self.filter_reset]

	def set_student_id(self, _student_id: int):
		self.current_student_id = _student_id

	def checkInput(self, temp, temp_list):
		result = self.int_convert_check(temp)
		if result is False:
			return False
		if int(temp) >= len(temp_list):
			print("Input number out of range (not an available command.)")
			result = False
		return result

	def int_convert_check(self, value) -> bool:
		"""Returns true if conversion is possible otherwise false"""
		result = True
		try:
			value = int(value)
		except Exception:
			print("Input a number for command usage.")
			result = False
		return result

	def command_print(self, current_text, list_index):
		print(f"\n-------------{self.title_text[list_index]}--------------")
		for index, text in enumerate(current_text):
			print(f"\t{index}. {text}")

	def login(self):
		students: list["Student"] = db_commands.get_students()
		while True:
			print("\n-------------LOGIN--------------")
			for index, text in enumerate(self.login_text):
				print(f"\t{index}. {text}")
			user_input = input("Input given: ")
			if self.checkInput(user_input, self.login_text):
				if int(user_input) == 2:  # Exit
					break
				username = input("Input Username:")
				if int(user_input) == 0:  # login
					for student in students:
						if student.Name == username:
							self.set_student_id(student.StudentID)
							self.main_interface()
					if students == []:
						print("User login not found.")

				elif int(user_input) == 1:  # Create user
					name_in_use = False
					for student in students:
						if student.Name == username.lower():
							print("Username already in use.")
							name_in_use = True
							break
					if not name_in_use:
						db_commands.create_student(username)
						students = db_commands.get_students()

	def main_interface(self):
		while True:
			self.command_print(self.main_text, 0)

			command = input("Input given: ")

			if not self.checkInput(command, self.main_text):
				continue
			if self.main_text[int(command)] == "Exit":  # exit
				break

			for index, _ in enumerate(self.main_text):
				if int(command) == index:
					self.main_func[index]()
					continue

	def manage_courses(self):
		while True:
			self.command_print(self.all_courses_text, 1)

			command = input("Input given: ")

			if not self.checkInput(command, self.all_courses_text):
				continue
			if self.all_courses_text[int(command)] == "Exit":  # exit
				break

			for index, _ in enumerate(self.all_courses_text):
				if int(command) == index:
					self.all_courses_func[index]()
					continue

	def manage_programs(self):
		while True:
			self.command_print(self.all_programs_text, 2)

			command = input("Input given: ")

			if not self.checkInput(command, self.all_programs_text):
				continue
			if self.all_programs_text[int(command)] == "Exit":  # exit
				break

			for index, _ in enumerate(self.all_programs_text):
				if int(command) == index:
					self.all_programs_func[index]()
					continue

	def manage_filters(self):
		while True:
			self.command_print(self.filters_text, 3)

			command = input("Input given: ")

			if not self.checkInput(command, self.filters_text):
				continue
			if self.filters_text[int(command)] == "Exit":  # exit
				break

			for index, _ in enumerate(self.filters_text):
				if int(command) == index:
					self.filters_func[index]()
					continue

	def view_selected_courses(self):
		selected_courses = db_commands.get_student_enrollment(self.current_student_id)
		print("---------------------YOUR SELECTED COURSES:------------------------")
		for element in selected_courses:
			print(element)

	def add_course_to_student(self):
		while True:
			course_id = input("Input CourseID (q to stop): ")
			if course_id.lower() == "q":
				break

			course_list: list["Course"] = db_commands.get_courses(self.current_student_id)
			student_list: list[str] = db_commands.get_student_enrollment(self.current_student_id)

			for course in course_list:
				if course.id == course_id.upper():  # course exists
					if len(student_list) == 0 or course not in student_list:  # if course not in studentenrollment: add
						db_commands.add_to_student_enrollment(self.current_student_id, course_id)

	def remove_course_from_student(self):
		while True:
			course_id = input("Input CourseID (q to stop): ")
			if course_id.lower() == "q":
				break

			student_list: list[str] = db_commands.get_student_enrollment(self.current_student_id)

			for course in student_list:
				if course in student_list:  # if course not in studentenrollment: add
					db_commands.remove_from_student_enrollment(self.current_student_id, course_id)

	def view_all_courses(self):
		selected_courses: list["Course"] = db_commands.get_courses(self.current_student_id)
		courses_dict = {}
		print("-----ALL COURSES------")
		print("Course | Credits")
		for element in selected_courses:
			element.print_course_oneliner()
			courses_dict[element.id] = element

		while True:
			user_input = input("Input CourseID (q to stop): ")
			if user_input.lower() == "q":
				break

			elif user_input in courses_dict.keys():
				print(courses_dict[user_input])

	def add_program_to_student(self):
		programs: list["Program"] = db_commands.get_programs()
		valid_program = False
		while not valid_program:
			user_input = input("Set program (q to exit): ")
			if user_input == "q":
				return
			if not self.int_convert_check(user_input):
				continue
			if any(program.id == int(user_input) for program in programs):
				valid_program = True
			else:
				print(f"There is no program {user_input}")
		cursor = cvars.conn.cursor()
		cursor.execute("UPDATE Students SET ProgramID = %s WHERE StudentID = %s", (int(user_input), self.current_student_id))
		cvars.conn.commit()
		cursor.close()
		return

	def remove_program_from_student(self):
		choice = ""
		while True:
			choice = input("Do you really want to remove the current program (y/n): ")
			if choice == "y":
				break
			elif choice == "n":
				break
		if choice == "y":
			cursor = cvars.conn.cursor()
			cursor.execute("UPDATE Students SET ProgramID = %s WHERE StudentID = %s", (None, self.current_student_id))
			cursor.close()
			cvars.conn.commit()
		return

	def view_all_programs(self):
		programs: list["Program"] = db_commands.get_programs()
		print("\n------------- Available Programs -------------")
		for program in programs:
			print(f"Program {program.id}", end=" | ")
			print(f"Credits {program.credits}")
		print("------------------------------------------------")

	def filter_subjects(self):
		pass

	def filter_points(self):
		pass

	def filter_reset(self):
		pass


def main():
	interface = Interface()
	interface.start_interface()


if __name__ == "__main__":
	main()
