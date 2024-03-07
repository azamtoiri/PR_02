from database.database import UserDatabase
from database.models import Users


def test_add_user():
    a = UserDatabase()
    user = Users(username='test_admin', password='test_password')
    assert a.insert_user(user) == True


def test_delete_user():
    a = UserDatabase()
    del_user = a.filter_user(username='test_admin')
    a.session.delete(del_user[0])
    a.session.commit()
    assert a.filter_user(username='test_admin') == []
