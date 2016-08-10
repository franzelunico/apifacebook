from __future__ import unicode_literals
from django.db import models


class TokenInfo(models.Model):
    token = models.CharField(max_length=255)
    expires = models.CharField(max_length=225, default="-1")

    def __str__(self):
        return self.token


class User(models.Model):
    fb_id = models.CharField(max_length=255)
    fb_first_name = models.CharField(max_length=255)
    fb_last_name = models.CharField(max_length=255)
    fb_email = models.EmailField(max_length=255)
    fb_birthday = models.DateField()
    fb_education = models.CharField(max_length=255)
    fb_name = models.CharField(max_length=255)
    fb_location = models.CharField(max_length=255)

    def __str__(self):
        return self.fb_name
