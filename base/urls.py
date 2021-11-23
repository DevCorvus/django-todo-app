from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/<str:uuid>/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about, name='about'),

    path('create-group/', views.create_group, name='create_group'),
    path('groups/', views.groups, name='groups'),
    path('groups/<str:uuid>/', views.show_group, name='show_group'),
    path('groups/<str:uuid>/edit/', views.update_group, name='update_group'),
    path('groups/<str:uuid>/delete/', views.delete_group, name='delete_group'),
    path('groups/<str:uuid>/send-message/', views.send_message, name='send_message'),
    path('groups/<str:uuid>/messages/', views.group_messages, name='group_messages'),
    path('groups/<str:uuid>/members/', views.group_members, name='group_members'),
    path('groups/<str:group_uuid>/delete-member/<str:member_uuid>', views.delete_member, name='delete_member'),
    path('delete-message/<str:uuid>/', views.delete_message, name='delete_message'),
    path('create-task/<str:uuid>/', views.create_group_task, name='create_group_task'),

    path('create-task/', views.create_task, name='create_task'),
    path('tasks/<str:uuid>/', views.show_task, name='show_task'),
    path('toggle-task-done/<str:uuid>/', views.toggle_task_done, name='toggle_task_done'),
    path('update-task/<str:uuid>/', views.update_task, name='update_task'),
    path('delete-task/<str:uuid>/', views.delete_task, name='delete_task'),
]
