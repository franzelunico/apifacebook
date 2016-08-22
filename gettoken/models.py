# encoding:utf-8
from django.db import models


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
    scholl_type = models.CharField(max_length=255)
    school_name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.school_name

    def setValues(self, values):
        res = School()
        if School.objects.filter(school_id=values["id"]).exists():
            res = School.objects.get(school_id=values["id"])
        res.school_id = values["id"]
        res.school_type = "Defult type"
        for key, value in values.iteritems():
            if key == "school":
                scholl = values[key]
                for key_s, value_s in scholl.iteritems():
                    if key_s == "name":
                        res.school_name = scholl[key_s]
        res.save()
        return res


class Concentration(models.Model):
    concentration_id = models.CharField(max_length=255)
    education_type = models.CharField(max_length=255)
    concentration_name = models.CharField(max_length=255)
    concentration_school = models.ForeignKey('School')

    def __unicode__(self):
        return self.concentration_name

    def setConcentration(self, values):
        res = Concentration()
        if values == "vacio":
            res = Concentration.objects.get(concentration_name="vacio")
            return res
        query_c = Concentration.objects.filter(concentration_id=values["id"])
        if query_c.exists():
            res = Concentration.objects.get(concentration_id=values["id"])
        res.concentration_id = values["id"]
        res.education_type = values["type"]
        res.concentration_name = values["concentration"][0]["name"]
        schol = School()
        res.concentration_school = schol.setValues(values)
        res.save()
        return res


class Education(models.Model):
    school = models.ForeignKey('School', on_delete=models.CASCADE,)
    concentration = models.ForeignKey('Concentration')

    def __unicode__(self):
        cad = self.school.__unicode__()
        cad += self.concentration.__unicode__()
        return cad

    def setValues(self, v_school, v_concentration):
        res = Education()
        res_s = School()
        res_c = Concentration()
        res.school = res_s.setValues(v_school)
        res.concentration = res_c.setConcentration(v_concentration)
        res.save()
        return res


class User(models.Model):
    fb_id = models.CharField(max_length=255)
    fb_first_name = models.CharField(max_length=255)
    fb_last_name = models.CharField(max_length=255)
    fb_email = models.EmailField(max_length=255)
    fb_birthday = models.DateField()
    fb_education = models.CharField(max_length=255)
    fb_name = models.CharField(max_length=255)
    fb_location = models.ForeignKey('Location', on_delete=models.CASCADE,)

    def __unicode__(self):
        return self.fb_name

    def setEducation(self, values):
        education = Education()
        if len(values) == 2:
            education = education.setValues(values[0], values[1])
        else:
            education = education.setValues(values[0], "vacio")
        return education
