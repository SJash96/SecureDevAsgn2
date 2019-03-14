from django.db import models
from datetime import datetime
from django.conf import settings

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
    thread_Exposer = models.CharField(default='NULL', max_length=200)
    thread_Expire = models.CharField(default='NULL', max_length=200)
    thread_Share = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='thread_Share')
    created_At = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return self.thread_Name
    class Meta:
        verbose_name_plural = "Threads"
