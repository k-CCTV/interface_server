from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post', views.post, name='post'),
    path('post/<int:id>', views.detail, name='detail'),
    path('post/edit/<int:id>',views.edit, name='edit'),
    path('post/delete/<int:id>',views.delete, name='delete'),
]