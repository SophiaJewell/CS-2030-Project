'''
user.py
this will hold the following:
- User class that is the base class for any students inputting information
- Admin class that is for admins of the database to be able to go in and adjust/modify/or remove entries
- Student user class that is inheriting the user class  that is view only access

All of this file is goaled to list out the
roles that is the main goal here. and ensure they communicate
as they are intended with the database and the GUI when GUI is completed.
'''

# Start with user class
class user:
    #Initializer to have the attributes listed out in database_handler.py on line 173
    def __init__(self,email,password_hash,role):
        self.__email = email
        self.__password_hash = password_hash
        self.__role = role

    #getters and setters for the roles within User
    def getemail(self):
        return self.__email
    def setemail(self,email):
        self.__email = email
    def getpassword_hash(self):
        return self.__password_hash
    def setpassword_hash(self,password_hash):
        self.__password_hash = password_hash
    def getrole(self):
        return self.__role

    #Use to_dict to return the values so database_handler can see and use them
    def to_dict(self):
        return {
            "email": self.__email,
            "password": self.__password_hash,
            "role": self.__role
        }
#Move onto Admin Class, Inheriting from the user class
class admin (user):
    def __init__(self,email,password_hash,admin_id,phone):
        super().__init__(email,password_hash,"admin")
        self.__admin_id = admin_id
        self.__phone = phone

    #Getters and setters for admin_id and phone
    def getadmin_id(self):
        return self.__admin_id
    def getphone(self):
        return self.__phone
    def setphone(self,phone):
        self.__phone = phone

    #to_dict method to return values for databae_handler
    def to_dict(self):
        together = super().to_dict()
        together["admin_id"] = self.__admin_id
        together["phone"] = self.__phone
        return together
#Studentuser class is next
class studentuser(user):
    def __init__(self,email,password_hash,student_id):
        super().__init__(email,password_hash,"user")
        self.__student_id = student_id

    #getters and setters
    def getstudent_id(self):
        return self.__student_id

    #to_dict time!
    def to_dict(self):
        collective = super().to_dict()
        collective["student_id"] = self.__student_id
        return collective