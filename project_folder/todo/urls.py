from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create_todo/', views.create_todo, name='create_todo'),
    path('delete_todo', views.delete_todo, name='delete_todo')
]