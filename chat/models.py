# from datetime import timezone
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

from PIL import Image


class Room(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, blank=True)

    def get_users_count(self):
        return self.users.count()

    def join(self, user):
        self.users.add(user)
        self.save()

    def leave(self, user):
        self.users.remove(user)
        self.save()

    def __str__(self):
        return f'{self.name} ({self.get_users_count()})'


class Message(models.Model):
    message = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save_message(self, user, room, message):
        timestamp = timezone.now()
        message_obj = Message(user=user, room=room, message=message, timestamp=timestamp)
        message_obj.save()

    @staticmethod
    def get_chat_history(room):
        return Message.objects.filter(room=room).order_by('timestamp') #new

    def __str__(self):
        return f'{self.user.username}: {self.message} [{self.timestamp}]'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def save_profile(self, phone):
        Profile(phone=phone).save()
