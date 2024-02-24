from database.database import Users, UserDatabase


def add_user(username: str, password: str) -> bool:
    try:
        user = Users(
            username=username,
            password=password,
        )
        user_db = UserDatabase()
        test = user_db.insert_user(user)
        return True
    except Exception as ex:
        print(ex)
        return False


if __name__ == '__main__':
    username = input('Имя пользователя: ')
    password = input('пароль: ')

    add_user(username, password)