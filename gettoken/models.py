# encoding:utf-8
from django.db import models
import datetime


class TokenInfo(models.Model):
    token = models.CharField(max_length=255, default="vacio")
    expires = models.CharField(max_length=225, default="-1")

    def __unicode__(self):
        return self.expires


class Location(models.Model):
    # Current city
    location_id = models.CharField(max_length=255, default="vacio")
    location_name = models.CharField(max_length=255, default="vacio")

    def __unicode__(self):
        return self.location_name


class School(models.Model):
    school_id = models.CharField(max_length=255, default="vacio")
    school_type = models.CharField(max_length=255, default="vacio")
    school_name = models.CharField(max_length=255, default="vacio")

    def __unicode__(self):
        return self.school_name


class User(models.Model):
    fb_id = models.CharField(max_length=255, default="vacio")
    fb_first_name = models.CharField(max_length=255, default="vacio")
    fb_last_name = models.CharField(max_length=255, default="vacio")
    fb_email = models.EmailField(max_length=255, default="vacio@gmail.com")
    fb_birthday = models.DateField(default=datetime.date.today)
    fb_name = models.CharField(max_length=255, default="vacio")
    fb_token = models.ForeignKey('TokenInfo')
    fb_location = models.ForeignKey('Location')
    # fb_education = models.ForeignKey('School')

    def __unicode__(self):
        return self.fb_name
