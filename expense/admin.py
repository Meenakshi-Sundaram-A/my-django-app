from django.contrib import admin
from .models import ExpenseDb,ExpenseSplit
# Register your models here.

admin.site.register(ExpenseDb)
admin.site.register(ExpenseSplit)