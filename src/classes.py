from constants.imports import gen


class Course:
	id: str
	credits: int
	education_level: str
	subjects: list[tuple[str, str]]
	study_period: int
	teaching_language: str

	def __init__(self, _subjects: list[tuple[str, str]], _level: str, _sp: 1, _tl: str):
		self.subjects = _subjects
		self.education_level = _level
		self.id = self.subjects[0][1] + next(gen.id_gen)
		self.credits = gen.credit_gen.send(self.education_level)
		self.study_period = _sp
		self.teaching_language = _tl

	def __str__(self):
		out = "Course:"
		out += f"\n\tCourseID: {self.id}"
		out += f"\n\tCredits: {self.credits}"
		out += f"\n\tEducation Level: {self.education_level}"
		out += "\n\tSubject: "
		for subject in self.subjects:
			out += subject[0]
			out += " "
		out += f"\n\tStudy Period: {self.study_period}"
		out += f"\n\tTeaching Language: {self.teaching_language}"
		return out
