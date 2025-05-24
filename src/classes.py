import src.gen as gen
import random as rand


class Course:
	id: str
	credits: int
	education_level: str
	subjects: list[tuple[str, str]]
	study_period: int
	teaching_language: str
	requirement_courses: list["Course"]

	def __init__(self, _id: str, _cr: int, _level: str, _sp: 1, _tl: str, _subjects: list[tuple[str, str]], _rc: list["Course"]):
		self.subjects = _subjects
		self.education_level = _level
		self.id = _id
		self.credits = _cr
		self.study_period = _sp
		self.teaching_language = _tl
		self.requirement_courses = _rc

	def print_course_oneliner(self):
		print(f"{self.id}, {self.credits}")

	def __str__(self):
		out = "Course:"
		out += f"\n\tCourseID: {self.id}"
		out += f"\n\tCredits: {self.credits}"
		out += f"\n\tEducation Level: {self.education_level}"
		out += "\n\tSubject: "
		for item in self.subjects:
			if isinstance(item, tuple) and len(item) == 2:
				first, second = item
				out += first + ", " + second
			else:
				first = item[0]
				out += first

		out += f"\n\tStudy Period: {self.study_period}"
		out += f"\n\tTeaching Language: {self.teaching_language}"
		if isinstance(self.requirement_courses, list):
			out += "\n\tRequirement Courses: "
			for course in self.requirement_courses:
				out += course.id
				out += ", "
		return out

	def __eq__(self, _other: "Course"):
		return self.id == _other.id

	def get_values(self):
		"""
		Gets all values as a tuples except subjects and requirement courses\n
		Return (id, credits, education_level, study_period, teaching_language)
		"""
		return (self.id, self.credits, self.education_level, self.study_period, self.teaching_language)

	def get_subjects(self):
		return self.subjects

	def get_requirement_courses(self):
		return self.requirement_courses

	def set_requirement_courses(self, courses: list):
		self.requirement_courses = courses


class Program:
	id: int
	credits: int
	course_list: list["Course"]

	def __init__(self):
		self.id = next(gen.prog_gen)
		self.credits = [180, 300][rand.randint(0, 1)]
		self.course_list = []

	def get_values(self):
		return (self.id, self.credits)

	def get_courses(self):
		return self.course_list


class Student:
	StudentID: int
	Name: str
	ProgramID: int

	def __init__(self, sql_tuple: tuple):
		self.StudentID = sql_tuple[0]
		self.Name = sql_tuple[1]
		self.ProgramID = sql_tuple[2]
