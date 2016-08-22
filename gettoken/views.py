from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import User, Location
import facebook
from dateutil import parser
import pprint


fb_app_id = '930344197111872'
scope = "&scope=user_about_me,email,user_birthday,user_education_history"
scope += ",user_location"


def index_view(request):
    if request.method == 'GET':
        return render(request, 'gettoken/index.html')
    elif request.method == 'POST':
        redir = "http://locales.code.bo/token/"
        urls = "https://www.facebook.com/dialog/oauth?+client_id="
        urls += fb_app_id+"&response_type=token"+"&redirect_uri="+redir
        urls += scope
        res = HttpResponseRedirect(urls)
        return res


def savetoken(request, youtoken, youexpires):
    graph = facebook.GraphAPI(access_token=youtoken, version='2.7')
# https://developers.facebook.com/docs/graph-api/reference/v2.7/user
    scope = "id,name,first_name,last_name,email,birthday,education,location"
    profile = graph.get_object(id='me', fields=scope)
    location = Location()
    user = User()
    if User.objects.filter(fb_id=profile["id"]).exists():
        user = User.objects.get(fb_id=profile["id"])
    else:
        user = User()
    if Location.objects.filter(location_id=profile["location"]["id"]).exists():
        location = Location.objects.get(location_id=profile["location"]["id"])
    else:
        location = Location()
    location.location_id = profile["location"]["id"]
    location.location_name = profile["location"]["name"]
    location.save()

    user.fb_id = profile["id"]
    user.fb_first_name = profile["first_name"]
    user.fb_last_name = profile["last_name"]
    user.fb_email = profile["email"]
    user.fb_birthday = parser.parse(profile["birthday"]).date()
    user.fb_education = "Defaul Value"
    if profile.has_key("education"):
        user.setEducation(profile["education"])
        existe(profile["education"])
    user.fb_name = profile["name"]
    user.fb_location = location
    user.save()
    return HttpResponseRedirect("http://locales.code.bo/token/")


def existe(list_education):
    pprint.pprint(list_education)
    # for item in list_education:
    #     pprint.print item
