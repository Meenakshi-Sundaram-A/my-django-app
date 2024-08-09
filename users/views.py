from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.postgres.search import SearchVector
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . models import FriendsGroup, Friend
from . forms import SplitGroup
from django.db.models import Q


# Create your views here.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

@login_required
def searchFriends(request):
    search_query = request.POST.get('search_query', '')
    users = User.objects.none() 

    if search_query:
        users = User.objects.filter(username__icontains=search_query).exclude(id=request.user.id)
    return render(request,'searchfriends.html',{'users':users})

@login_required
def addFriend(request,user_id):

    friend = get_object_or_404(User,id = user_id)
    if not Friend.objects.filter(user=request.user, friends=friend).exists():
        Friend.objects.create(user=request.user,friends=friend)
    if not Friend.objects.filter(user=friend, friends=request.user).exists():
        Friend.objects.create(user=friend,friends=request.user)

    return redirect('display_friends')

@login_required
def displayFriends(request):
    friends = Friend.objects.filter(user=request.user)
    
    return render(request,'displayfriends.html',{'friends':friends})

@login_required
def createGroup(request):
    if request.method == "POST":
        form = SplitGroup(request.POST,user = request.user)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.save()
            form.save_m2m()
            grouptemp = FriendsGroup.objects.get(id=group.id)
            grouptemp.friends.add(request.user)
            return redirect("display_groups")
    else:
        form = SplitGroup(user = request.user)
    return render(request,'creategroup.html',{"form":form})


@login_required
def displayGroups(request):
    user = request.user
    groups = FriendsGroup.objects.filter( 
        Q(creator = user) | Q(friends = user)
    ).distinct()
    view_group_id = request.GET.get('view_group_id')
    return render(request,'displaygroup.html',{"groups":groups,"view_group_id":view_group_id})

@login_required
def editGroup(request,group_id):
    group = get_object_or_404(FriendsGroup,id = group_id)
    if request.user != group.creator and request.user not in group.friends.all():
        return redirect("display_groups")
    if request.method == "POST":
        form = SplitGroup(request.POST, instance=group, user = request.user)
        if form.is_valid():
            form.save()
            grouptemp = FriendsGroup.objects.get(id=group.id)
            grouptemp.friends.add(request.user)
            return redirect("display_groups")
    else:
        form = SplitGroup(instance=group, user = request.user)
    friends = group.friends.all() 
    return render(request,'editgroup.html',{"form": form, "friends": friends, "group": group})

@login_required
def deleteGroup(request,group_id):
    group = get_object_or_404(FriendsGroup,id = group_id)
    if request.user != group.creator:
        return redirect("display_groups")
    if request.method == "POST":
        group.delete()
        return redirect("display_groups")  # Redirect to a list of groups or another page
    return render(request, 'confirmdelete.html', {"group": group})