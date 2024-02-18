import flet as ft
from flet_route import Params, Basket


def RequestsView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    """Requests view"""
    title = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Text('Все заявки', size=25)])

    def search(e: ft.ControlEvent):
        ...

    search_field = ft.TextField(expand=True, hint_text='Поиск')
    search_field.on_submit = lambda e: search(e)

    all_requests = ft.ListView()

    content = ft.Column()
    content.controls.append(title)
    content.controls.append(ft.Row([search_field]))

    return ft.View(
        route='/requests',
        controls=[content]
    )


def RequestCreateView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    title = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Text('Создать Заявку', size=25)])

    content = ft.Column()
    content.controls.append(title)

    return ft.View(
        route='/request/create',
        controls=[content]
    )
