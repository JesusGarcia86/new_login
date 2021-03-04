from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_reroute),
    path('login', views.login),
    path('create_user', views.register),
    path('log_in', views.log_in),
    path('wall', views.sucess),
    path('create_message', views.create_mess),
    path('create_comment', views.create_comm),
    path('logout', views.logout),
    path('user/<int:user_id>', views.profile),
    path('delete/<int:mess_id>', views.delete_mess),
    path('comm_delete/int:comm_id', views.delete_comm),
    path('like/<int:user_id>', views.add_like),
    path('edit/<int:id>', views.edit),
    path('update/<int:id>', views.update),
]