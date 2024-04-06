from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm,SetPasswordForm
from django.contrib.auth.views import PasswordResetView,PasswordResetConfirmView
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.http import urlsafe_base64_decode
from .chatbot import Chatbot



def send_confirmation_email(user):
    subject = 'Account Confirmation'
    message = 'Thank you for signing up!:\n\n'
    from_email = '' 
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)

def student_signup(request):
    if request.method == 'POST':
        form = StudentCreationForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.role = CustomUser.STUDENT
            student.save()

            login(request, student)

            send_confirmation_email(student)

            messages.success(request, ' registration successful')
            return redirect('student_dashboard') 
        else:
            messages.error(request, 'Error in student registration. Please correct the errors below.')
    else:
        form = StudentCreationForm()
    return render(request, 'authentication/student_signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('student_dashboard')  
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'authentication/login.html', {'form': form})


def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    view = PasswordResetConfirmView.as_view(
        template_name='authentication/password_reset_confirm.html',
        success_url='/reset/done/', 
        form_class=SetPasswordForm,
    )

    return view(request, uidb64=uidb64, token=token, extra_context={'user': user})

def my_logout(request):
    logout(request)
    return redirect('login')    

def counselor_signup(request):
    pass

def home(request):
    return render(request, 'authentication/login.html')



def counselor_dashboard(request):
    return render('home')



chatbot = Chatbot()

@login_required
def chat_list(request):
    chatbot_username = "deepcare"

    chatbot_chats = Chat.objects.filter(user=request.user, chatbot__username=chatbot_username)

    if not chatbot_chats.exists():
        chatbot_user = CustomUser.objects.get(username=chatbot_username)
        chatbot_chat = Chat.objects.create(user=request.user, chatbot=chatbot_user)

        initial_message_content = "Hello, I'd like to start a conversation!"
        initial_message = Message.objects.create(chat=chatbot_chat, sender=request.user, content=initial_message_content)

        chatbot_response = chatbot.respond(initial_message_content)
        bot_message = Message.objects.create(chat=chatbot_chat, sender=chatbot_chat.chatbot, content=chatbot_response)

        chatbot_chats = [chatbot_chat]

    return render(request, 'chat/chat_list.html', {'chatbot_chats': chatbot_chats})


@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, user=request.user)
    messages = chat.messages.all()
    form = MessageForm()


    chatbot_username = "Shambapp"

    chatbot_chats = Chat.objects.filter(user=request.user, chatbot__username=chatbot_username)

    if not chatbot_chats.exists():
        chatbot_user = CustomUser.objects.get(username=chatbot_username)
        chatbot_chat = Chat.objects.create(user=request.user, chatbot=chatbot_user)

        initial_message_content = " "
        initial_message = Message.objects.create(chat=chatbot_chat, sender=request.user, content=initial_message_content)

        chatbot_response = chatbot.respond(initial_message_content)
        bot_message = Message.objects.create(chat=chatbot_chat, sender=chatbot_chat.chatbot, content=chatbot_response)

        chatbot_chats = [chatbot_chat]

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.sender = request.user
            message.save()

            if message.sender == request.user:
                chatbot_response = chatbot.respond(message.content)
                bot_message = Message.objects.create(chat=chat, sender=chat.chatbot, content=chatbot_response)

    return render(request, 'chat/chat_detail.html', {'chat': chat, 'messages': messages, 'form': form,'chatbot_chats': chatbot_chats})

@login_required
def chat_create(request):
    chatbot_username = "shambapp"

    chatbot_user = CustomUser.objects.get(username=chatbot_username)
    chatbot_chat = Chat.objects.create(user=request.user, chatbot=chatbot_user)

    initial_message_content = "Hello, I'd like to start a conversation!"
    initial_message = Message.objects.create(chat=chatbot_chat, sender=request.user, content=initial_message_content)

    chatbot_response = chatbot.respond(initial_message_content)
    bot_message = Message.objects.create(chat=chatbot_chat, sender=chatbot_chat.chatbot, content=chatbot_response)

    return redirect('chat_detail', chat_id=chatbot_chat.id)

@login_required
def chat_delete(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, user=request.user)
    chat.delete()
    return redirect('chat_list')


