from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


   
class CustomUser(AbstractUser):
    STUDENT = 'student'
    COUNSELOR = 'counselor'
    
    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (COUNSELOR, 'Counselor'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)
    slug = models.SlugField(unique=True, blank=True)
    email_confirmed = models.BooleanField(default=False)
    confirmation_code = models.CharField(max_length=255, null=True, blank=True)

    groups = models.ManyToManyField('auth.Group',verbose_name='groups',blank=True,related_name='custom_user_groups')
    user_permissions = models.ManyToManyField('auth.Permission',verbose_name='user permissions',blank=True,related_name='custom_user_permissions')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)


class Chat(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_chats')
    chatbot = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='chatbot_chats')
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
