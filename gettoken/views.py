from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import User
from django.core.exceptions import ObjectDoesNotExist
import facebook
from dateutil import parser


fb_app_id = 'you app id'
# token = "EAACEdEose0cBAE4FSTzZC944nXcEdemr8aebrayu49c81JBQRYzwnlr3dcQH8aW77lLnCwRnSWP9ebTqAWCMVfcxq5GCSPUIREk0yoP9bX0lksKrtsBSdMYRUX69AD5ZCdSdY8Bk4nG3d13PWIIVAZCJeD6R0YpTPwZCrZCcughStMIiR06HB"
# defaul ,id ,name ,first_name ,last_name ,age_range ,link ,gender ,locale
# picture ,timezone ,updated_time ,verified
# scope define permisos para el token
# ref https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow#login
# lista de permisos permitidos
# https://developers.facebook.com/docs/facebook-login/permissions/
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
    print profile
    user = User()
    try:
            user = User.objects.get(fb_id=profile["id"])
    except ObjectDoesNotExist:
            user = User()
            user.fb_id = profile["id"]
    user.fb_first_name = profile["first_name"]
    user.fb_last_name = profile["last_name"]
    user.fb_email = profile["email"]
    user.fb_birthday = parser.parse(profile["birthday"]).date()
    user.fb_education = profile["education"]
    user.fb_name = profile["name"]
    user.fb_location = profile["location"]
    user.save()
    return HttpResponseRedirect("http://locales.code.bo/token/")
