'''
student.py
this section includes the following:
 - StudentRecord class with:
    1.student_id
    2.first_name
    3.last_name
    4.age
    5.gender
    6.phone
-GradeManager class with:

'''
import statistics

#Start with writing student record class
class studentrecord:
    def __init__(self,student_id,first_name,last_name,age,gender,phone):
        self.__student_id = student_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.setage(age)
        self.__gender = gender
        self.__phone = phone

    #Getter and setter time!
    def getstudent_id(self):
        return self.__student_id
    def getfirst_name(self):
        return self.__first_name
    def setfirst_name(self,first_name):
        self.__first_name = first_name
    def getlast_name(self):
        return self.__last_name
    def setlast_name(self,last_name):
        self.__last_name = last_name
    def getage(self):
        return self.__age
    def setage(self,age):
        if not (16 <= age <= 100):
            raise ValueError("Sorry! Age must be between 16 and 100.")
        self.__age = age
    def getgender(self):
        return self.__gender
    def setgender(self,gender):
        self.__gender = gender
    def getphone(self):
        return self.__phone
    def setphone(self,phone):
        self.__phone = phone

    #need to_dict and now need from_dict() which is the reverse of to_dict
    # and allows it to be created into a studentrecord object
    def to_dict(self):
        return {
            "student_id": self.__student_id,
            "first_name": self.__first_name,
            "last_name": self.__last_name,
            "age": self.__age,
            "gender": self.__gender,
            "phone": self.__phone
        }

    #from dict also needs to be a static method so this can be its own method and
    #python cannot confuse info for self and cause errors.
    @staticmethod
    def from_dict(info):
        return studentrecord(
            info["student_id"],
            info["first_name"],
            info["last_name"],
            info["age"],
            info["gender"],
            info["phone"]
        )

#time to start Grademanager class!
class grademanager:
    def __init__(self,student_id):
        self.__student_id = student_id
        self.__grades = []

    # getter for id and a getter and setter for grades
    def getstudent_id(self):
        return self.__student_id
    def getgrades(self):
        return self.__grades
    def setgrades(self,grades):
        self.__grades = grades

    #A method to add a course to a student record
    def add_course(self,course_name):
        self.__grades.append([course_name,[]])

    #A method to add grades to the course
    def add_grade(self, course_name, grade):
        for row in self.__grades:
            if row [0] == course_name:
                row[1].append(grade)

    #Method for calculating the average
    def calculate_average(self,course_name):
        for row in self.__grades:
            if row [0] == course_name:
                return statistics.mean(row[1])

    def convert_to_letter(self,avg):
        if avg >= 90:
            return 'A'
        elif avg >= 80:
            return 'B'
        elif avg >= 70:
            return 'C'
        elif avg >= 60:
            return 'D'
        elif avg >= 0:
            return 'F'

    #to_dict method to save to JSON
    def to_dict(self):
        return {
            "student_id": self.__student_id,
            "grades": self.__grades
        }

    #from_dict ti go to database handler
    @staticmethod
    def from_dict(info):
       gm = grademanager(info["student_id"])
       gm.setgrades(info["grades"])
       return gm
