from django.urls import path

from .views import (
    upload_and_calculate,
    login_view,
    register_view,
    logout_view,
    CalculationListView,
    CalculationDetailView,
    CalculationCreateView,
    CalculationUpdateView,
    CalculationDeleteView,
    home_page,
)

urlpatterns = [
    path('', upload_and_calculate, name='home'),   # щоб був перехід на головну сторінку
    path('upload_and_calculate/', upload_and_calculate, name='upload_and_calculate'),
    path('feedback/', home_page, name='feedback'),
    path('login/', login_view, name="login"),
    path('register/', register_view, name="register"),
    path('logout/', logout_view, name="logout"),
    path('calculations/', CalculationListView.as_view(), name="calculation_list"),
    path('calculations/create/', CalculationCreateView.as_view(), name="calculation_create"),
    path('calculations/<int:pk>/', CalculationDetailView.as_view(), name="calculation_detail"),
    path('calculations/<int:pk>/edit/', CalculationUpdateView.as_view(), name="calculation_edit"),
    path('calculations/<int:pk>/delete/', CalculationDeleteView.as_view(), name="calculation_delete"),
]


