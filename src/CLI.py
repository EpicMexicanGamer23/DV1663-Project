"""Command Line Interface (to get database)"""
from src.classes import Course
# import main


class Interface:
    # Courses = Course()
    # conn = main.conn

    def __init__(self):
        self.user_logins = {}
        self.login_text = ["Login", "Create User", "Exit"]

        self.main_text = ["View Course Settings", "View Programs", "Filters", "View Courses Selected", "Exit"]

        self.all_courses_text = ["Add Course", "Remove Course", "View All Courses", "Back To Previous", "Exit"]
        self.all_courses_func = [self.add_course, self.remove_course, self.view_all_courses, self.back_up]

        self.all_programs_text = ["Add Program", "Remove Program", "View All Programs", "Back To Previous", "Exit"]
        self.all_programs_func = [self.add_program, self.remove_program, self.view_all_programs, self.back_up]

        self.filters_text = ["Filter By Course Subjects", "Filter By Course Points", "Reset Filters", "Back To Previous", "Exit"]
        self.filters_func = [self.filter_subjects, self.filter_points, self.filter_reset, self.back_up]


    
    def checkInput(self, temp):
        result = True
        try:
            temp = int(temp)
        except Exception:
                print("Input a number for command usage.")
                result = False
            
        if(temp >= len(self.main_text)):
            print("Input number out of range (not an available command.)")
            result = False
        return result
    
    def command_print(self, current_text):
        print("\nAvailable commands: ")
        for index,text in enumerate(current_text):
            print(f"\t{index}. {text}")

#reminder: login is only checking for a user now, need to associate "Selected courses" with specific login (and only show for that user)
    def login(self):
        while(True):
            self.command_print(self.login_text)
            login = input("Input command: ")
            if(self.checkInput(login)):
                username = input("Input Username:")
                password = input("Input password:")
                if(int(login) == 1):
                    if (username in self.user_logins and self.user_logins[username] == password):
                        self.main_interface()
                    else:
                        print("Incorrect password.")
                elif (int(login) == 2):
                    if username not in self.user_logins:
                        self.user_logins[username] = password
                    else:
                        print("user already exists.")
                else:
                    break


    def main_interface(self, text, func):
        while(True):
            command = self.command_print(text)

            if not self.checkInput(command):
                continue
            if(text[command] == "Exit" ):    #exit
                break
            
            for index, _ in enumerate(text):
                if (command == index):
                    if(self.all_commands_list[index] != []):
                        self.main_interface(self.all_text_list[index+1], self.all_commands_list[index+1])
                    continue

    def add_course(self):
        pass

    def remove_course(self):
        pass

    def view_all_courses(self):
        pass

    def add_program(self):
        pass

    def remove_program(self):
        pass

    def view_all_programs(self):
        pass

    def filter_subjects(self):
        pass

    def filter_points(self):
        pass

    def filter_reset(self):
        pass


    def courses_selected_view(self):
        #program chosen: program_2 || [NO CHOSEN PROGRAM]
        # Courses \nMa1448 [ECST, Subjects]\n, ...
        cursor = self.conn.cursor()

        view_selection = """ SELECT * FROM ´StudentEnrollment´"""
        cursor.execute(view_selection)
        



def main():
    interface = Interface()
    interface.start_interface()

if __name__ == "__main__":
	main()

