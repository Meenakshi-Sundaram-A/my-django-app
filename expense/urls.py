from django.urls import path
from . import views

urlpatterns = [
    # path("create/",views.create_expense,name="create_expense"),
    # path("",views.display_expense,name="display_expenses"),
    path('create_expense/<int:group_id>/', views.create_expense, name='create_expense'),
    path('display_expenses/', views.display_expenses, name='display_expenses'),
    path("delete/<int:expense_id>",views.delete_expense,name = "delete_expense"),
]
    