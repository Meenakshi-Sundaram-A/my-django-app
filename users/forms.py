# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from . models import FriendsGroup,Friend

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
class SplitGroup(forms.ModelForm):
    class Meta:
        model = FriendsGroup
        fields = ['group_name', 'friends']
        widgets = {
            'friends': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SplitGroup, self).__init__(*args, **kwargs)
        self.fields['group_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['friends'].widget.attrs.update({'class': 'form-check'})
        if user:
            friends_queryset = Friend.objects.filter(user=user).values_list('friends', flat=True)
            self.fields['friends'].queryset = User.objects.filter(id__in=friends_queryset)

