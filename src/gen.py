import random as rand
import math as math

from constants.variables import COURSE_SUBJECTS, EDUCATION_LEVELS, LANGUAGES
from src.classes import Course, Program


def gen_course_code():
	for num in range(0, 10000):  # Get a course code, maximum of 10000 courses
		yield f"{num:04d}"  # Return the course code as a 4 digit string i.e int 1 -> 0001


def gen_program_code():
	for num in range(0, 10000):
		yield num


def gen_course_credits(level: str):
	while True:
		if level == EDUCATION_LEVELS[1]:  # If the course is a second-cycle course
			return 8
		return rand.randrange(2, 6, 2)


id_gen = gen_course_code()
next(id_gen)

prog_gen = gen_program_code()
next(prog_gen)


def create_fc_course() -> "Course":
	subjects = rand.sample(COURSE_SUBJECTS, rand.randint(1, 2))
	education_level = EDUCATION_LEVELS[0]
	study_period = rand.randint(1, 4)
	language = LANGUAGES[rand.randint(0, len(LANGUAGES) - 1)]
	course_id = subjects[0][1] + next(id_gen)
	credits = gen_course_credits(education_level)
	new_course = Course(course_id, credits, education_level, study_period, language, subjects, [])
	return new_course


def create_sc_course() -> "Course":
	subjects = rand.sample(COURSE_SUBJECTS, rand.randint(1, 2))
	education_level = EDUCATION_LEVELS[1]
	study_period = rand.randint(1, 4)
	language = LANGUAGES[rand.randint(0, len(LANGUAGES) - 1)]
	course_id = subjects[0][1] + next(id_gen)
	credits = gen_course_credits(education_level)
	new_course = Course(course_id, credits, education_level, study_period, language, subjects, [])
	return new_course


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
		course_id = subjects[0][1] + next(id_gen)
		credits = gen_course_credits(education_level)
		new_course = Course(course_id, credits, education_level, study_period, language, subjects, [])
		courses.append(new_course)
	# Secondly we create the remaining courses
	for _ in range(90):
		subjects = rand.sample(COURSE_SUBJECTS, rand.randint(1, 2))
		education_level = EDUCATION_LEVELS[rand.randint(0, 1)]
		study_period = rand.randint(1, 4)
		language = LANGUAGES[rand.randint(0, len(LANGUAGES) - 1)]
		course_id = subjects[0][1] + next(id_gen)
		credits = gen_course_credits(education_level)
		new_course = Course(course_id, credits, education_level, study_period, language, subjects, [])
		if (rand.random() < requirement_multiplier) or (education_level == EDUCATION_LEVELS[1]):
			req_amount = rand.randint(1, requirement_max)
			if len(courses) < req_amount:
				req_amount = len(courses)
			req_courses = rand.sample(courses, req_amount)
			new_course.set_requirement_courses(req_courses)
		courses.append(new_course)

	return courses


def generate_program() -> "Program":
	sc_courses = []
	fc_courses = []
	total_credits = 0
	program_credits = [180, 300][rand.randint(0, 1)]
	for _ in range(10):
		new_course = create_sc_course()
		total_credits += new_course.credits
		sc_courses.append(new_course)

	index = 0
	while program_credits - total_credits > 6:  # While we are still able to create the largest possible first-cycle course
		sc_course: "Course" = sc_courses[index]
		new_course = create_fc_course()
		fc_courses.append(new_course)
		req_courses = sc_course.get_requirement_courses()
		req_courses.append(new_course)
		sc_course.set_requirement_courses(req_courses)  # Add the requirement course to the course
		total_credits += new_course.credits  # Increase the total amount of credits created
		index += 1
		if index == len(sc_courses):
			index = 0

	# At this point we need to add a course with the difference in points
	credits_left = program_credits - total_credits
	extra_course = create_fc_course()
	extra_course.credits = credits_left
	fc_courses.append(extra_course)
	new_program = Program((next(prog_gen), program_credits))
	new_program.set_course_list(fc_courses + sc_courses)
	return new_program
