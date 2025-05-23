import mysql.connector as mysql

COURSE_SUBJECTS = [
	("Mathematics", "MA"),
	("Physics", "FY"),
	("Technology", "TE"),
	("Economics", "IY"),
	("Computer Science", "PA"),
	("Software Engineering", "PA"),
	("Electrical Engineering", "ET"),
	("Mechanical Engineering", "MT"),
	("Media Technology", "ME"),
	("Spatial Planning", "FM"),
]

EDUCATION_LEVELS = ["First-cycle", "Second-cycle"]


LANGUAGES = ["Swedish", "English"]

# variables:
# conn: mysql.MySQLConnection = None
conn: mysql.MySQLConnection = None
username: str = None
mysqlpassword = None
