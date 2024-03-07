from flet_route import path

from views import RequestsView, RequestCreateView, RequestDetailView, ClientCreateView, LoginView, ClientSearch
from views.status_view import StatusView

all_routes = [
    path(url='/login', clear=False, view=LoginView),
    path(url='/requests', clear=False, view=RequestsView),
    path(url='/request/create', clear=False, view=RequestCreateView),
    path(url='/request/:id', clear=False, view=RequestDetailView),

    path(url='/create/client', clear=False, view=ClientCreateView),
    path(url='/client/search', clear=False, view=ClientSearch),

    path(url='/statistic', clear=False, view=StatusView)
]
