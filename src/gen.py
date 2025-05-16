import random as rand

from constants.variables import EDUCATION_LEVELS


def gen_course_code():
	for num in range(0, 10000):  # Get a course code, maximum of 10000 courses
		yield f"{num:04d}"  # Return the course code as a 4 digit string i.e int 1 -> 0001


def gen_course_credits():
	level = ""
	while True:
		if level == EDUCATION_LEVELS[1]:  # If the course is a second-cycle course
			level = yield 8
		level = yield rand.randrange(2, 6, 2)


id_gen = gen_course_code()
next(id_gen)
credit_gen = gen_course_credits()
next(credit_gen)
