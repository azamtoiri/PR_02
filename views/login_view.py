import flet as ft
from flet_route import Params, Basket


def LoginView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    title = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Text('Вход', size=25)])

    username_field = ft.TextField(hint_text='Имя пользователя')

    password_field = ft.TextField(hint_text='Пароль')
    password_field.password = True
    password_field.can_reveal_password = True

    login_button = ft.OutlinedButton(text='Вход')
    login_button.on_click = lambda _: page.go('/requests')

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
