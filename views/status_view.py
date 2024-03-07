import flet as ft
from flet_route import Basket, Params

from database.database import RequestDatabase
from user_controls import BackButton

r_db = RequestDatabase()
dlg = ft.AlertDialog()


def open_dlg(e: ft.ControlEvent, text: str) -> None:
    e.page.dialog = dlg
    dlg.title = ft.Text(text)
    dlg.open = True
    e.page.update()


def count_done_req(requests) -> int:
    count = 0
    for request, responsible, state in requests:
        if state.state_name == 'выполнено':
            count += 1
        else:
            continue
    return count


def StatusView(page: ft.Page, params: Params, basket: Basket) -> ft.View:
    title = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Text('Страница статистики', size=25)])
    # region: help data Status
    requests = r_db.get_requests_with_res_and_state()

    done_requests = count_done_req(requests)

    unique_types_of_faults = r_db.get_unique_types_of_faults()
    # endregion

    type_of_faults_text = ft.Text('Типы Ошибок и их количество', size=20)
    type_of_faults_text = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[type_of_faults_text])

    statistics_list = ft.ListView()
    statistics_list.spacing = 10

    for type_of_fault, count in unique_types_of_faults:
        statistics_list.controls.append(
            ft.Row(controls=[ft.Text(f'Тип ошибки: {type_of_fault}'), ft.Text(f'Количество: {count}')]))

    done_requests_text = ft.Text(f'Количество завершенных заявок: {done_requests}')

    content = ft.Column()
    content.controls.append(title)
    content.controls.append(type_of_faults_text)
    content.controls.append(ft.Row(alignment=ft.MainAxisAlignment.END, controls=[done_requests_text]))
    content.controls.append(ft.Column(alignment=ft.MainAxisAlignment.CENTER, controls=[statistics_list]))

    content.controls.append(ft.Row(alignment=ft.MainAxisAlignment.END, controls=[BackButton('Назад')]))

    return ft.View(
        scroll=ft.ScrollMode.AUTO,
        route='/status',
        controls=[
            content
        ]
    )
