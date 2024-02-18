import flet as ft


class RequestCard(ft.UserControl):
    def __init__(self, title: str, description: str, url: str) -> None:
        super().__init__()
        self.title = title
        self.description = description
        self.url = url

    def build(self) -> ft.Column:
        main = ft.ListTile()
        main.title = ft.Text(self.title)
        main.subtitle = ft.Text(self.description)

        detail_button = ft.ElevatedButton('Перейти')
        detail_button.on_click = lambda _: self.page.go(self.url)

        buttons = ft.Row(alignment=ft.MainAxisAlignment.END)
        buttons.controls.append(detail_button)

        column = ft.Column()
        column.controls.append(main)
        column.controls.append(buttons)

        _main_card = ft.Card(
            content=column
        )

        return ft.Column(
            [_main_card]
        )


class BackButton(ft.UserControl):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def go_back(self, e: ft.ControlEvent) -> None:
        self.page.route = self.page.views[-2].route
        self.page.update()

    def build(self):
        return ft.ElevatedButton(
            text=self.name,
            on_click=lambda e: self.go_back(e)
        )
