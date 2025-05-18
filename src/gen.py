import random as rand

from constants.variables import COURSE_SUBJECTS, EDUCATION_LEVELS, LANGUAGES
from src.classes import Course


def gen_course_code():
	for num in range(0, 10000):  # Get a course code, maximum of 10000 courses
		yield f"{num:04d}"  # Return the course code as a 4 digit string i.e int 1 -> 0001


def gen_course_credits(level: str):
	while True:
		if level == EDUCATION_LEVELS[1]:  # If the course is a second-cycle course
			return 8
		return rand.randrange(2, 6, 2)


id_gen = gen_course_code()
next(id_gen)


def generate_100_courses() -> list:
	courses = []
	requirement_multiplier = 0.1
	requirement_max = 3
	# First we create 10 courses that are certainly First-cycle courses as a foundation
	for _ in range(10):
		subjects = rand.sample(COURSE_SUBJECTS, rand.randint(1, 2))
		education_level = EDUCATION_LEVELS[0]
		study_period = rand.randint(1, 4)
		language = LANGUAGES[rand.randint(0, len(LANGUAGES) - 1)]
		new_course = Course(subjects, education_level, study_period, language)
		courses.append(new_course)
	# Secondly we create the remaining courses
	for _ in range(90):
		subjects = rand.sample(COURSE_SUBJECTS, rand.randint(1, 2))
		education_level = EDUCATION_LEVELS[rand.randint(0, 1)]
		study_period = rand.randint(1, 4)
		language = LANGUAGES[rand.randint(0, len(LANGUAGES) - 1)]
		new_course = Course(subjects, education_level, study_period, language)
		if (rand.random() < requirement_multiplier) or (education_level == EDUCATION_LEVELS[1]):
			req_amount = rand.randint(1, requirement_max)
			if len(courses) < req_amount:
				req_amount = len(courses)
			req_courses = rand.sample(courses, req_amount)
			new_course.set_requirement_courses(req_courses)
		courses.append(new_course)

	return courses
