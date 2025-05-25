"""Command Line Interface (to get database)"""

from src.classes import Course, Student, Program
import constants.variables as cvars
import src.DB_commands as db_commands


class Interface:
	def __init__(self):
		self.current_student_id = None
		self.login_text = ["Login", "Create User", "Exit"]
		self.title_text = ["MENU", "COURSE MANAGEMENT", "PROGRAM MANAGEMENT", "FILTERS"]

		self.main_text = ["View Course Settings", "View Program Settings", "View Selection", "Exit"]
		self.main_func = [self.manage_courses, self.manage_programs, self.view_selected_courses]

		self.all_courses_text = ["Add Course", "Remove Course", "View All Courses", "Filter Settings", "Exit"]

		self.all_courses_func = [self.add_course_to_student, self.remove_course_from_student, self.view_all_courses, self.manage_filters]

		self.all_programs_text = ["Set Program", "Remove Program", "View All Programs", "Exit"]
		self.all_programs_func = [self.add_program_to_student, self.remove_program_from_student, self.view_all_programs]

		self.filters_text = ["Filter By Course Subjects", "Filter By Course Points", "Filter By Program", "Reset Filters", "Exit"]
		self.filters_func = [self.filter_subjects, self.filter_points, self.filter_programs, self.filter_reset]

		self.f_subjects = []
		self.f_points = []
		self.f_programs = []

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
				username = input("Input Username: ")
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
						db_commands.add_to_student_enrollment(self.current_student_id, course.id)

	def remove_course_from_student(self):
		while True:
			course_id = input("Input CourseID (q to stop): ")
			if course_id.lower() == "q":
				break

			student_list: list[str] = db_commands.get_student_enrollment(self.current_student_id)

			for course in student_list:
				if course in student_list:  # if course not in studentenrollment: add
					db_commands.remove_from_student_enrollment(self.current_student_id, course_id)

	def __helper_filter_subject__(self, course: "Course"):
		subjects_str: str = course.get_subjects()  # Get the subjects returned from the sql query as "Subject1, Subject2, etc.."
		subjects = subjects_str.split(",")  # Split the string into ["Subject1", "Subject2"]
		for index, subject in enumerate(subjects):
			subjects[index] = subject.replace(" ", "")  # Remove potential spaces in the subject string
		for subject in subjects:
			if subject in self.f_subjects:
				return True
		return False

	def __helper_filter_points__(self, course: "Course"):
		if course.credits in self.f_points:
			return True
		return False

	def __helper_filter_program__(self, course: "Course"):
		pass

	def view_all_courses(self):
		selected_courses: list["Course"] = db_commands.get_courses(self.current_student_id)
		if len(self.f_subjects) != 0:
			filtered_courses = list(filter(self.__helper_filter_subject__, selected_courses))
			selected_courses = filtered_courses
		if len(self.f_points) != 0:
			filtered_courses = list(filter(self.__helper_filter_points__, selected_courses))
			selected_courses = filtered_courses
		if len(self.f_programs) != 0:
			program_courses = db_commands.get_program_courses(self.f_programs)
			in_program = lambda x: x.id in program_courses
			filtered_courses = list(filter(in_program, selected_courses))
			selected_courses = filtered_courses
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
		while True:
			print("\n------------- Subject Filter --------------")
			print("Includes all courses with either of the options")
			for index, subject in enumerate(cvars.COURSE_SUBJECTS):
				if subject[0] in self.f_subjects:
					print(f"[X] {index}. {subject[0]}")
				else:
					print(f"[ ] {index}. {subject[0]}")
			user_input = input("Enter subject number to filter by (q to exit): ")
			if user_input == "q":
				break
			if not self.checkInput(user_input, cvars.COURSE_SUBJECTS):
				continue
			else:
				if cvars.COURSE_SUBJECTS[int(user_input)][0] in self.f_subjects:
					self.f_subjects.remove(cvars.COURSE_SUBJECTS[int(user_input)][0])
				else:
					self.f_subjects.append(cvars.COURSE_SUBJECTS[int(user_input)][0])

	def filter_points(self):
		available_points = [2, 4, 6, 8]
		while True:
			print("\n------------- ECTS Point Filter --------------")
			print("Includes all courses with either of the options")
			for index, point in enumerate(available_points):
				if point in self.f_points:
					print(f"[X] {index}. {point}")
				else:
					print(f"[ ] {index}. {point}")
			user_input = input("Enter point index to filter by (q to exit): ")
			if user_input == "q":
				break
			if not self.checkInput(user_input, available_points):
				continue
			else:
				if [2, 4, 6, 8][int(user_input)] in self.f_points:
					self.f_points.remove(available_points[int(user_input)])
				else:
					self.f_points.append(available_points[int(user_input)])

	def filter_programs(self):
		programs: list["Program"] = db_commands.get_programs()
		while True:
			print("\n------------- Program Filter --------------")
			print("Includes all courses with either of the options")
			for index, program in enumerate(programs):
				if program.id in self.f_programs:
					print(f"[X] {index}. Program {program.id}")
				else:
					print(f"[ ] {index}. Program {program.id}")
			user_input = input("Enter program index to filter by (q to exit): ")
			if user_input == "q":
				break
			if not self.checkInput(user_input, programs):
				continue
			else:
				if programs[int(user_input)].id in self.f_programs:
					self.f_programs.remove(programs[int(user_input)].id)
				else:
					self.f_programs.append(programs[int(user_input)].id)

	def filter_reset(self):
		self.f_points = []
		self.f_subjects = []
		self.f_programs = []
		return


def main():
	interface = Interface()
	interface.start_interface()


if __name__ == "__main__":
	main()
