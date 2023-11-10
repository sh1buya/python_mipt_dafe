from datetime import datetime
from string import punctuation
class User:
    def __init__(self, nickname, mail, birth, password, last_action) -> None:
        self.nickname = nickname
        self.mail = mail
        self.birth = birth
        self.password = password
        self.last_action = datetime.today().strftime("%Y-%m-%d")

    def update_action(self):
        self.last_action = datetime.today().strftime("%Y-%m-%d")
    def get_info(self):
        print( f"Nickname = {self.nickname} \n \
        Mail = {self.mail} \n \
        Birth = {self.birth} \n \
        Last_action = {self.last_action}")
    
        self.update_action()

class DataBase:
    def __init__(self) -> None:
        self.data = []
        self.nicknames = set()
        self.mails = set()

    def check_nickname(self, nickname):
        if nickname.lower() in self.nicknames:
            raise ValueError("not unique")
        if not( 2<=len(nickname)<=10):
            raise ValueError("wrong size")
        if nickname[0].isdigit() or not(nickname.isalnum and nickname.isascii):
            raise ValueError("invalid user")
        

    def check_password(self, password:str):
        upper = False
        digit = False
        lower = False
        punct = False

        for char in password:
            if char.isascii():
                if char.isupper():
                    upper = True
                elif char.islower():
                    lower = True
                elif char.isdigit():
                    digit = True
                elif char in punctuation:
                    punct = True
                else:
                    raise ValueError("invalid symbol in password")
            else:
                raise ValueError("invalid symbol in password")
        if not (upper*digit*lower*punct):
            raise ValueError("password s not protected enough")
        if len(password) < 8:
            raise ValueError("too short password")
    def check_mail(self, mail):
        if mail[-13:] != "@phystech.edu":
            raise ValueError("invalid mail")
        if mail in self.mails:
            raise ValueError("not unique mail")
        if mail.count("@") !=1:
            raise ValueError("invalid mail")
    def check_birth(self, birth):
        today = datetime.today().date()
        if int(today - birth )/365<18:
            raise ValueError("user under 18 y.o.")

    def add_user(self, nickname, password, mail, birth):
        birth = datetime.today().strftime("%Y-%m-%d").date()
        self.check_nickname(nickname)
        self.check_birth(birth)
        self.check_mail(mail)
        self.check_password(password)

        self.mails.add(mail)
        self.nicknames.add(nickname)

        self.data.append(User(nickname, password, mail, birth))

    def del_user(self, id):
        self.data[id] = None
    def user_info(self, id):
        self.data[id].get_info()

    def change_data(self, id, changes):
        user = self.data[id]
        for key, value in changes.item():
            if key == "nickname":
                self.check_nickname(value)
                self.nicknames.remove(user.nickname)
                user.nickname = value
                self.nickname.add(value)
            elif key == "password":
                self.check_password(value)
                user.password = value
            elif key == "mail":
                self.check_mail(value)
                self.mails.remove(user.mail)
                user.mail = value ###############
                self.mails.add(value)
        self.data[id] = user
        self.data[id].update_action()

    def update(self):
        self.data[id].update_action()
