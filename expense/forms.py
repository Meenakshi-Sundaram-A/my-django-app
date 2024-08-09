from django import forms
from . models import ExpenseDb, FriendsGroup , SPLIT_CHOICE
from django.contrib.auth.models import User
from django import forms
from django.db.models import Q

class ExpenseForm(forms.ModelForm):

    class Meta:
        model = ExpenseDb
        fields = ['amount', 'description', 'paid_by', 'split_type']
        widgets = {
            "split_type":forms.Select(choices=SPLIT_CHOICE, attrs={'id': 'id_split_type'}),
        }
    
    def __init__(self,*args,**kwargs):
        group = kwargs.pop('group',None)
        super(ExpenseForm,self).__init__(*args,**kwargs)
        if group:
            self.fields['paid_by'].queryset = group.friends.all()
            self.fields['paid_by'].empty_label = "Select User"