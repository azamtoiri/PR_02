from flet_route import path

from views.login_view import LoginView
from views.requests_view import RequestsView, RequestCreateView, RequestDetailView

all_routes = [
    path(url='/login', clear=False, view=LoginView),
    path(url='/requests', clear=False, view=RequestsView),
    path(url='/request/create', clear=False, view=RequestCreateView),
    path(url='/request/:id', clear=False, view=RequestDetailView),
]