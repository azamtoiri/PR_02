import flet as ft
from flet_route import Routing

from views.routes import all_routes
from database.database import BaseDatabase


def main(page: ft.Page) -> None:
    # init database
    BaseDatabase()

    page.theme_mode = 'light'
    Routing(page=page, app_routes=all_routes)
    page.on_route_change = Routing.change_route

    page.go('/login')


ft.app(target=main)
