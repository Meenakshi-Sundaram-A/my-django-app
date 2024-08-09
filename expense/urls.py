from django.urls import path
from . import views

urlpatterns = [
    path('create_expense/<int:group_id>/', views.create_expense, name='create_expense'),
    path('display_expenses/', views.display_expenses, name='display_expenses'),
    path("delete/<int:expense_id>",views.delete_expense,name = "delete_expense"),
]
    