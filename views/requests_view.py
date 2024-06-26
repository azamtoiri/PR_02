import datetime
import random
import time

import flet as ft
from flet_route import Params, Basket

from database.database import RequestDatabase, UserDatabase
from database.models import Requests
from user_controls import RequestCard, BackButton

# initializing databases
rdb = RequestDatabase()
udb = UserDatabase()
dlg = ft.AlertDialog()


def open_dlg(e: ft.ControlEvent, text: str) -> None:
    e.page.dialog = dlg
    dlg.title = ft.Text(text)
    dlg.open = True
    e.page.update()


def RequestsView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    """Requests view"""
    title = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Text('Все заявки', size=25)])
    requests_ = rdb.get_all_requests()

    def add_requests():
        for request in requests_:
            all_requests.controls.append(
                RequestCard(request.type_of_fault, request.description, f'/request/{request.request_id}',
                            request_number=request.request_number))

    def search(e: ft.ControlEvent):
        search_val = str(search_field.value).strip() if len(search_field.value) else None
        if search_val is None:
            all_requests.controls.clear()
            add_requests()
            e.page.update()
            return 0
        _req = rdb.get_request_by_request_number(search_val)
        print(_req)
        if _req:
            all_requests.controls.clear()
            for req in _req:
                all_requests.controls.append(
                    RequestCard(req.type_of_fault, req.description, f'/request/{req.request_id}',
                                request_number=req.request_number))
                e.page.update()
        else:
            all_requests.controls.clear()
            e.page.update()

    request_add_button = ft.ElevatedButton('Создать заявку')
    request_add_button.on_click = lambda _: page.go('/request/create')
    find_client_button = ft.ElevatedButton('Найти клиента')
    find_client_button.on_click = lambda _: page.go('/client/search')
    statistic_button = ft.ElevatedButton('Посмотреть статистику')
    statistic_button.on_click = lambda _: page.go('/statistic')

    search_field = ft.TextField(expand=True, hint_text='Поиск')
    search_field.input_filter = ft.NumbersOnlyInputFilter()
    search_field.on_submit = lambda e: search(e)

    all_requests = ft.ListView()
    add_requests()

    content = ft.Column()
    content.controls.append(title)
    content.controls.append(ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[find_client_button]))
    content.controls.append(ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[request_add_button, statistic_button]))
    content.controls.append(ft.Row([search_field]))
    content.controls.append(all_requests)
    content.controls.append(ft.Row(alignment=ft.MainAxisAlignment.END,
                                   controls=[ft.ElevatedButton('Выход', on_click=lambda _: page.go('/login'))]))

    return ft.View(
        route='/requests',
        controls=[content],
        scroll=ft.ScrollMode.AUTO
    )


def RequestCreateView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    title = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Text('Создать Заявку', size=25)])
    dlg = ft.AlertDialog()

    def open_dlg(e: ft.ControlEvent, text: str, field: ft.TextField = None) -> None:
        page.dialog = dlg
        dlg.title = ft.Text(text)
        if field:
            field.value = ""
        dlg.open = True
        e.page.update()

    def add_request(e: ft.ControlEvent) -> None:
        request_number = str(request_number_field.value).strip()
        equipment = str(equipment_filed.value).strip()
        date = str(date_field.value).strip()
        client = str(client_field.value).strip()
        description = str(description_field.value).strip()
        type_of_fault = str(type_of_fault_field.value).strip()
        responsible = str(responsible_field.value).strip()

        client_id = e.page.session.get('client_id')
        request_state = str(request_state_field.value).strip()
        state_id = rdb.get_state_id(request_state).state_id

        responsible_id = rdb.get_responsible_by_name(responsible).responsible_id
        req = Requests(
            request_number=request_number,
            client_id=client_id,
            state_id=state_id,
            responsible_id=responsible_id,
            equipment=equipment,
            type_of_fault=type_of_fault,
            description=description
        )
        _status_req = rdb.add_request(req)
        if _status_req:
            open_dlg(e, 'Заявка успешно добавлена')
            time.sleep(1)
            e.page.route = '/requests'
        else:
            open_dlg(e, 'Ошибка')

    def generate_number(e: ft.ControlEvent) -> None:
        request_number_field.value = random.randint(1, 100000000)
        e.page.update()

    def set_name_by_id(e: ft.ControlEvent) -> None:
        client_id = str(client_field.value).strip()
        page.session.set('client_id', client_id)
        client_name = rdb.get_client_by_id(client_id)
        if client_name:
            client_field.value = client_name.client_name
        else:
            open_dlg(e, 'Нет такого пользователя', client_field)
        e.page.update()

    # States
    states_of_request = ['в ожидании', 'в работе', 'выполнено']

    # region: Fields
    request_number_field = ft.TextField(hint_text='Номер заявки', expand=True)
    request_number_field.disabled = True
    equipment_filed = ft.TextField(hint_text='Оборудование', expand=True)
    responsible_field = ft.Dropdown(hint_text='Ответственный', expand=True)
    date_field = ft.TextField(hint_text=datetime.date.today().strftime("%d-%m-%Y"), disabled=True, expand=True)
    type_of_fault_field = ft.TextField(hint_text='Тип неисправности', expand=True)
    description_field = ft.TextField(hint_text='Описание', expand=True)
    client_field = ft.TextField(hint_text='ID клиента', expand=True)
    client_field.input_filter = ft.NumbersOnlyInputFilter()
    client_field.on_submit = lambda e: set_name_by_id(e)

    request_state_field = ft.Dropdown(hint_text='Статус заявки', expand=True)
    for state in states_of_request:
        request_state_field.options.append(ft.dropdown.Option(state))

    responsibles = rdb.get_responsible()
    for responsible in responsibles:
        responsible_field.options.append(ft.dropdown.Option(responsible.responsible_name))
    # endregion

    add_button = ft.ElevatedButton('Добавить', on_click=lambda e: add_request(e))
    random_number_button = ft.IconButton(ft.icons.SECURITY, on_click=lambda e: generate_number(e))
    client_add_button = ft.IconButton(ft.icons.PERSON_ADD)
    client_add_button.on_click = lambda _: page.go('/create/client')

    content = ft.Column()
    content.controls.append(title)
    content.controls.append(ft.Row([request_number_field, ft.Text('Сгенерировать номер заявки'), random_number_button]))
    content.controls.append(ft.Row([equipment_filed, date_field]))
    content.controls.append(ft.Row([client_field, client_add_button, description_field]))
    content.controls.append(ft.Row([type_of_fault_field, request_state_field]))
    content.controls.append(ft.Row([responsible_field]))
    content.controls.append(ft.Divider(color='black'))
    content.controls.append(ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[add_button]))
    content.controls.append(ft.Row(alignment=ft.MainAxisAlignment.END, controls=[BackButton('назад')]))

    return ft.View(
        route='/request/create',
        controls=[content]
    )


def RequestDetailView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    title = ft.Row(alignment=ft.MainAxisAlignment.CENTER,
                   controls=[ft.Text(f'Номер заявки {params.get("id")}', size=25, color=ft.colors.BLUE, )])

    def update_all(e: ft.ControlEvent):
        new_des = str(description.value).strip()
        rdb.update_description(params.get('id'), new_des)

        new_state = str(status_of_req.value).strip()
        rdb.update_request_state(params.get('id'), new_state)

        new_responsible = str(responsible.value).strip()
        rdb.update_responsible(params.get('id'), new_responsible)

        open_dlg(e, 'Успешно изменено')

    req = rdb.get_request_by_id(params.get('id'))

    type_of_fault = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Text(value=req.type_of_fault, size=20)])
    description = ft.TextField(value=req.description, expand=True, enable_suggestions=True)

    responsible = ft.Dropdown()
    responsible.hint_text = rdb.get_responsible_by_id(req.responsible_id).responsible_name
    responsibilies = rdb.get_responsible()
    for res in responsibilies:
        responsible.options.append(ft.dropdown.Option(res.responsible_name))

    status_of_req = ft.Dropdown()
    status_of_req.hint_text = rdb.get_state_by_id(req.state_id).state_name
    states = rdb.get_states()
    for state in states:
        status_of_req.options.append(ft.dropdown.Option(state.state_name))

    client_name = ft.Text(f'имя клиента: {rdb.get_client_by_id(req.client_id).client_name}', size=20)
    client_phone = ft.Text(f'Номер телефона: {rdb.get_client_by_id(req.client_id).phone_number}', size=20)

    create_at = ft.Text(value=f'Дата создания: {req.created_at.strftime("%d-%m-%Y")}')
    create_at.size = 20

    change_description_button = ft.ElevatedButton('Изменить описание')
    change_description_button.on_click = lambda e: update_all(e)

    content = ft.Column()
    content.controls.append(title)
    content.controls.append(ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Text('Тип ошибки',
                                                                                            size=15,
                                                                                            color=ft.colors.RED)]))
    content.controls.append(type_of_fault)
    content.controls.append(ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Text('Описание',
                                                                                            size=15,
                                                                                            color=ft.colors.GREEN)]))
    content.controls.append(ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[description]))
    content.controls.append(ft.Column([client_name, client_phone]))
    content.controls.append(ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[status_of_req]))
    content.controls.append(ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[responsible]))
    content.controls.append(ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[change_description_button]))
    content.controls.append(ft.Row(alignment=ft.MainAxisAlignment.END, controls=[create_at]))
    content.controls.append(ft.Row(alignment=ft.MainAxisAlignment.END, controls=[BackButton('Назад')]))

    return ft.View(
        route='/request/:id',
        controls=[content]
    )
