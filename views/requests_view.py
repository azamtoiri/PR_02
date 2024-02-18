import flet as ft
from flet_route import Params, Basket

from database.database import RequestDatabase, UserDatabase
from user_controls import RequestCard, BackButton

# initializing databases
rdb = RequestDatabase()
udb = UserDatabase()


def RequestsView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    """Requests view"""
    title = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Text('Все заявки', size=25)])

    def search(e: ft.ControlEvent):
        ...

    request_add_button = ft.ElevatedButton('Создать заявку')
    request_add_button.on_click = lambda _: page.go('/request/create')

    search_field = ft.TextField(expand=True, hint_text='Поиск')
    search_field.on_submit = lambda e: search(e)

    requests_ = rdb.get_all_requests()

    all_requests = ft.ListView()
    for request in requests_:
        all_requests.controls.append(
            RequestCard(request.type_of_fault, request.description, f'/request/{request.request_id}'))

    content = ft.Column()
    content.controls.append(title)
    content.controls.append(ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[request_add_button]))
    content.controls.append(ft.Row([search_field]))
    content.controls.append(all_requests)

    return ft.View(
        route='/requests',
        controls=[content]
    )


def RequestCreateView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    title = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Text('Создать Заявку', size=25)])

    content = ft.Column()
    content.controls.append(title)
    content.controls.append(ft.Row(alignment=ft.MainAxisAlignment.END, controls=[BackButton('назад')]))

    return ft.View(
        route='/request/create',
        controls=[content]
    )


def RequestDetailView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    title = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Text('Создать Заявку', size=25)])

    content = ft.Column()
    content.controls.append(title)
    content.controls.append(ft.Row(alignment=ft.MainAxisAlignment.END, controls=[BackButton('Назад')]))

    return ft.View(
        route='/request/:id',
        controls=[content]
    )
