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

	def __init__(self, _subjects: list[tuple[str, str]], _level: str, _sp: 1, _tl: str):
		self.subjects = _subjects
		self.education_level = _level
		self.id = self.subjects[0][1] + next(gen.id_gen)
		self.credits = gen.gen_course_credits(self.education_level)
		self.study_period = _sp
		self.teaching_language = _tl
		self.requirement_courses = []

	def __str__(self):
		out = "Course:"
		out += f"\n\tCourseID: {self.id}"
		out += f"\n\tCredits: {self.credits}"
		out += f"\n\tEducation Level: {self.education_level}"
		out += "\n\tSubject: "
		for subject in self.subjects:
			out += subject[0]
			out += ", "
		out += f"\n\tStudy Period: {self.study_period}"
		out += f"\n\tTeaching Language: {self.teaching_language}"
		out += "\n\tRequirement Courses: "
		for course in self.requirement_courses:
			out += course.id
			out += ", "
		return out

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
