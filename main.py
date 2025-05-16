from constants.imports import Course
from constants.variables import COURSE_SUBJECTS, EDUCATION_LEVELS


def main():
	my_course = Course([COURSE_SUBJECTS[0]], EDUCATION_LEVELS[0], 1, "Swedish")
	print(my_course)


if __name__ == "__main__":
	main()
