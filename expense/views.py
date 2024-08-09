from django.shortcuts import render,redirect,get_object_or_404, HttpResponse
from .forms import ExpenseForm
from . models import ExpenseDb,ExpenseSplit,User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from users.models import FriendsGroup

@login_required
def create_expense(request,group_id):
    group = get_object_or_404(FriendsGroup, id=group_id)
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.created_by = request.user
            expense.group_no = group

            if expense.split_type == "equal":
                total_amount = expense.amount
                num_members = group.friends.count()
                if num_members>0:
                    split_amount = total_amount/num_members
                    expense.save()
                    for member in group.friends.all():
                        ExpenseSplit.objects.create(
                            expense = expense,
                            user = get_object_or_404(User,username = member),
                            amount = split_amount,
                            group_name = group
                        )
            
            elif expense.split_type == "custom":
                total_amount = expense.amount
                total_split_amount = 0
                splits = []
                for member in group.friends.all():
                    split_amount = request.POST.get(f'split_amount_{member.id}',0)
                    total_split_amount+=float(split_amount)
                    splits.append((member,split_amount))

                if abs(total_amount-total_split_amount)!=0:
                    form.add_error(None,"The total amount and Total Split amount is not matching")
                    return render(request,'create_expense.html',{'form':form,'group':group})
                
                expense.save()
                for member,split_amount in splits:
                    ExpenseSplit.objects.create(
                        expense = expense,
                        user = member,
                        amount = split_amount,
                        group_name = group,
                    )

            elif expense.split_type == 'percentage':
                total_amount = expense.amount
                total_percentage = 0
                splits = []

                for member in group.friends.all():
                    percentage = request.POST.get(f'split_percentage_{member.id}',0)
                    total_percentage+=int(percentage)
                    splits.append((member,percentage))

                if total_percentage != 100:
                    form.add_error(None,"Total Percentage of the split is not equal to 100")
                    return render(request,"create_expense.html",{'form':form,'group':group})
                
                expense.save()
                for member,percentage in splits:
                    split_amount = total_amount * (int(percentage)/100)
                    ExpenseSplit.objects.create(
                        expense = expense,
                        group_name = group,
                        amount = split_amount,
                        user = member
                    )
            else: 
                expense.save()
            return redirect('display_groups')
    else:
        form = ExpenseForm(group=group)
    return render(request, 'create_expense.html', {'form': form,'group':group})

@login_required
def display_expenses(request):
    user_groups = FriendsGroup.objects.filter(friends=request.user)
    group_ids = user_groups.values_list('id', flat=True)
    user_expenses = ExpenseDb.objects.filter(group_no__id__in=group_ids)
    expense_splits = ExpenseSplit.objects.filter(expense__in=user_expenses, user=request.user)

    total_amount_pay = sum(split.amount for split in expense_splits)
    
    return render(request, 'display_expense.html', {'expenses': user_expenses, 'splits': expense_splits,'total_amount_pay':total_amount_pay})

@login_required
def delete_expense(request,expense_id):
    expense = get_object_or_404(ExpenseDb, id=expense_id)
    expense.delete()
    return redirect('display_expenses')
