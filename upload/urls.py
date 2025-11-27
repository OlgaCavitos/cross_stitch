from django.urls import path
from .views import (
    upload_and_calculate,
    login_view,
    register_view,
    logout_view,
    calculation_list,
    calculation_create,
    calculation_delete,
)

urlpatterns = [
    path('', upload_and_calculate, name='home'),
    path('upload_and_calculate/', upload_and_calculate, name='upload_and_calculate'),
    path('login/', login_view, name="login"),
    path('register/', register_view, name="register"),
    path('logout/', logout_view, name="logout"),
    path('calculations/', calculation_list, name="calculation_list"),
    path('calculations/create/', calculation_create, name="calculation_create"),
    path('calculations/delete/<int:pk>/', calculation_delete, name="calculation_delete"),
]


