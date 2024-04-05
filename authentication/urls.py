from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('', home, name="home"),
    path('student/signup/', student_signup, name='student_signup'),
    path('counselor/signup/', counselor_signup, name='counselor_signup'),
    path('', login_view, name='login'), 
    path('logout/',my_logout,name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='authentication/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'), name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>/',auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'), name='password_reset_complete'),
    path('chats/', chat_list, name='chat_list'),
    path('chats/<int:chat_id>/', chat_detail, name='chat_detail'),
    path('chats/create/', chat_create, name='chat_create'),
    path('chats/delete/<int:chat_id>/', chat_delete, name='chat_delete'),

]
