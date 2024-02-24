import time

import flet as ft
from flet_route import Params, Basket

from user_controls import BackButton, RequestCard, ClientCard
from database.database import RequestDatabase

rdb = RequestDatabase()


def ClientCreateView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    title = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Text('Добавить клиента')])
    dlg = ft.AlertDialog()

    # region: functions
    def open_dlg(e: ft.ControlEvent, text) -> None:
        e.page.dialog = dlg
        dlg.title = ft.Text(text)
        dlg.open = True
        e.page.update()

    def add_client(e: ft.ControlEvent) -> None:
        client_name = str(client_name_field.value).strip()
        phone = str(phone_field.value).strip()

        _added = rdb.add_client(client_name, phone)
        if _added:
            open_dlg(e, f"Успешно добавлено: id {_added.client_id}")
            time.sleep(2)
            e.page.route = e.page.views[-2].route
            e.page.update()
        else:
            open_dlg(e, 'Ошибка')
    # endregion

    # region: Fields
    client_name_field = ft.TextField(hint_text='Имя клиента', expand=True)
    phone_field = ft.TextField(hint_text='Номер телефона +7', expand=True)
    # endregion

    create_button = ft.ElevatedButton('Добавить')
    create_button.on_click = lambda e: add_client(e)

    content = ft.Column()
    content.controls.append(title)
    content.controls.append(ft.Row(controls=[client_name_field]))
    content.controls.append(ft.Row(controls=[phone_field]))
    content.controls.append(ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[create_button]))
    content.controls.append(ft.Row(alignment=ft.MainAxisAlignment.END, controls=[BackButton('Назад')]))
    return ft.View(
        route='/create/client',
        controls=[content]
    )


def ClientSearch(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    title = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Text('Поиск сотрудника', size=25)])

    def search(e: ft.ControlEvent) -> None:
        reses = rdb.get_client_by_fio(str(search_field.value).strip())
        if reses:
            result.controls.clear()
            for res in reses:
                tmp_text = f'Имя: {res.client_name}\nНомер Телефона {res.phone_number}'
                result.controls.append(ClientCard(f'ID: {res.client_id}', tmp_text, ''))
                e.page.update()
        else:
            result.controls.clear()
            result.controls.append(
                ft.Text('Такого пользователя нет', size=50, text_align="center"))

    search_field = ft.TextField(hint_text='Найти')
    search_field.helper_text = 'Введите фамилию'
    search_field.on_submit = lambda e: search(e)

    result = ft.ListView()
    result.spacing = 10
    _res = rdb.get_all_clients()
    for res in _res:
        tmp_text = f'Имя: {res.client_name}\nНомер Телефона {res.phone_number}'
        result.controls.append(ClientCard(f'ID: {res.client_id}', tmp_text, ''))

    content = ft.Column()
    content.controls.append(title)
    content.controls.append(ft.Row(alignment=ft.MainAxisAlignment.END, controls=[BackButton('Назад')]))
    content.controls.append(ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[search_field]))
    content.controls.append(result)

    return ft.View(
        route='/client/search',
        controls=[content],
        scroll=ft.ScrollMode.AUTO
    )
