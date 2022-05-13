from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('post', views.post, name='post'),
    path('test',views.test, name='test'),
    path('post/<int:id>', views.detail, name='detail'),
    path('post/edit/<int:id>',views.edit, name='edit'),
    path('post/delete/<int:id>',views.delete, name='delete'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
