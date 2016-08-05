from __future__ import unicode_literals
from django.db import models


class TokenInfo(models.Model):
    token = models.CharField(max_length=255)
    expires = models.CharField(max_length=225, default="-1")

    def __str__(self):
        return self.token


class User(models.Model):
    fb_name = models.CharField(max_length=255)
    fb_id = models.CharField(max_length=255)
