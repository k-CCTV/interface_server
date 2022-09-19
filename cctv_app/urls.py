from django.urls import path
from .views import *

board_list = BoardViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
board_create = BoardViewSet.as_view({
    'get': 'list',
    'post':'create'
})
board_detail = BoardViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})
board_modify = BoardViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
})

urlpatterns = [
    path('', board_list),
    path('create', board_create),
    path('board/<int:pk>/',board_detail),
    path('modify/<int:pk>/',board_modify),
   
]