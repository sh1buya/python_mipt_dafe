from base import DataBase

db = DataBase()

while True:
    cmd = input()
    try:
        if cmd == "add":
            nickname, password, mail, birth = input().split()
            db.add_user(nickname, password, mail, birth)
        elif cmd == "del":
            id = int(input())
            db.del_user(id)
        elif cmd == "change":
            id, key, value = input().split()
            db.change_data(int(id), {key:value})
        elif cmd == "info":
            id = int(input)
            db.update(id)
    except ValueError as er:
        print(er.massages())
