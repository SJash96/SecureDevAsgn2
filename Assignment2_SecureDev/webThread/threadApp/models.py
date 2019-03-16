from django.db import models
from datetime import datetime
from pytz import timezone
from django.conf import settings
from django.contrib.auth.models import User

expire_time = [
    ('10 mins', '10 Minutes'),
    ('1 hr', '1 Hour'),
    ('1 day', '1 Day'),
    ('1 week', '1 Week'),
]

expose = [
    ('public', 'Public'),
    ('private', 'Private'),
]


class Threads(models.Model):
    thread_Owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  default=1, related_name='thread_Owner')
    thread_Name = models.CharField(max_length=200)
    thread_Body = models.TextField()
    thread_Exposer = models.CharField(default='public', max_length=200)
    thread_Expire = models.CharField(default='10 mins', max_length=200)
    thread_TillExpire = models.CharField(default='', max_length=200)
    thread_Share = models.ManyToManyField(User, blank=True, null=True)
    created_At = models.DateTimeField(default=datetime.now().replace(tzinfo=timezone('UTC')))
    def __str__(self):
        return self.thread_Name
    class Meta:
        verbose_name_plural = "Threads"
