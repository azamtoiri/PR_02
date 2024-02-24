import flet as ft
from flet_route import Params, Basket

from database.database import UserDatabase

user_db = UserDatabase()
dlg = ft.AlertDialog()


def open_dlg(e: ft.ControlEvent, text: str) -> None:
    e.page.dialog = dlg
    dlg.title = ft.Text(text)
    dlg.open = True
    e.page.update()


def LoginView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    title = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Text('Вход', size=25)])

    def login_user(e: ft.ControlEvent):
        try:
            _login = user_db.login_user(username_field.value, password_field.value)
            if _login:
                e.page.route = '/requests'
                e.page.update()
            else:
                open_dlg(e, 'Не правильный логин или пароль')
        except Exception as ex:
            print(ex)

    username_field = ft.TextField(hint_text='Имя пользователя')

    password_field = ft.TextField(hint_text='Пароль')
    password_field.password = True
    password_field.can_reveal_password = True

    login_button = ft.OutlinedButton(text='Вход')
    login_button.on_click = lambda e: login_user(e)

    content = ft.Column()
    content.controls.append(title)
    content.controls.append(ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[username_field]))
    content.controls.append(ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[password_field]))
    content.controls.append(ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[login_button]))

    return ft.View(
        route='/login',
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        controls=[content]
    )
