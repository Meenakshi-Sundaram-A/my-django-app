from django.db import models
from django.contrib.auth.models import User
from users.models import FriendsGroup


SPLIT_CHOICE = (
    ('equal','Equal'),
    ('custom','Custom'),
    ('percentage','Percentage')
)
class ExpenseDb(models.Model):
    amount = models.IntegerField()
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    paid_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="expense_paid")
    split_type = models.CharField(max_length=10,choices=SPLIT_CHOICE,default='equal')
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="expenses_created",null=True)
    group_no = models.ForeignKey(FriendsGroup, on_delete=models.CASCADE,null=True)

    def __str__(self):
         return (f"Description: {self.description}, "
                f"Amount: {self.amount}, "
                f"Created Date: {self.created_date}, "
                f"Paid By: {self.paid_by.username}, "
                f"Split Type: {self.split_type}, "
                f"Created By: {self.created_by.username if self.created_by else 'N/A'}, "
                f"Group Number: {self.group_no},")
    
class ExpenseSplit(models.Model):
    expense = models.ForeignKey(ExpenseDb,on_delete=models.CASCADE,related_name="splits")
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    group_name = models.ForeignKey(FriendsGroup, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"{self.user.username} owes {self.amount} for {self.expense.description}"
