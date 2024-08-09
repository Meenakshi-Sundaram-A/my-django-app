from django.urls import path
from . import views
from .views import SignUpView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("search_friends/",views.searchFriends,name ="search_friends"),
    path("add_friend/<int:user_id>/",views.addFriend, name = "add_friend"),
    path("display_friends/",views.displayFriends,name = "display_friends"),
    path("create_group/",views.createGroup,name="create_group"),
    path("display_groups/",views.displayGroups,name="display_groups"),
    path('groups/<int:group_id>/edit/', views.editGroup, name='edit_group'),
    path('groups/<int:group_id>/delete/', views.deleteGroup, name='delete_group'),
]  



