from django.db import models
import json


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    num_sockets = models.IntegerField(default=0)

    def increment_socket(self):
        self.num_sockets += 1
        self.save()

    def decrement_socket(self):
        self.num_sockets -= 1
        self.save()

    class Meta:
        app_label = "user"
