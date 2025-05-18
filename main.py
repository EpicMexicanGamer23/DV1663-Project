import src.gen as gen


def main():
	my_courses = gen.generate_100_courses()
	for course in my_courses:
		print(course)


if __name__ == "__main__":
	main()
