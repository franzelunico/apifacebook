# encoding:utf-8
from django.db import models
from django.contrib.auth.models import User as UserDjango
import pprint


class TokenInfo(models.Model):
    token = models.CharField(max_length=255)
    expires = models.CharField(max_length=225, default="-1")

    def __unicode__(self):
        return self.token


class Location(models.Model):
    location_id = models.CharField(max_length=255)
    location_name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.location_name


class School(models.Model):
    school_id = models.CharField(max_length=255)
    school_type = models.CharField(max_length=255)
    school_name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.school_name

    def setValues(self, values):
        res = School()
        if School.objects.filter(school_id=values["id"]).exists():
            res = School.objects.get(school_id=values["id"])
            print "Existe"
        res.school_id = values["id"]
        res.school_type = values["type"]
        pprint.pprint(values)
        for key, value in values.iteritems():
            if key == "school":
                scholl = values[key]
                for key_s, value_s in scholl.iteritems():
                    if key_s == "name":
                        res.school_name = scholl[key_s]
        res.save()
        return res


class User(models.Model):
    fb_id = models.CharField(max_length=255)
    fb_first_name = models.CharField(max_length=255)
    fb_last_name = models.CharField(max_length=255)
    fb_email = models.EmailField(max_length=255)
    fb_birthday = models.DateField()
    fb_name = models.CharField(max_length=255)
    fb_education = models.ForeignKey('School')
    fb_location = models.ForeignKey('Location')
    fb_token = models.ForeignKey('TokenInfo')
    user = models.OneToOneField(UserDjango, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.fb_name

    def setEducation(self, values):
        v_school = values[0]
        res_s = School()
        res_s = res_s.setValues(v_school)
        return res_s
