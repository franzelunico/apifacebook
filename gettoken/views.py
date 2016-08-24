from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Location, TokenInfo, School
from .models import User as UserFb
from django.http import HttpResponse
from django.shortcuts import render_to_response
import facebook
from dateutil import parser
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User as UserDj
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect


fb_app_id = '930344197111872'
scope = "&scope=user_about_me,email,user_birthday,user_education_history"
scope += ",user_location"


@csrf_protect
def index(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            user_dj = UserDj.objects.get(pk=request.user.pk)
            user_fb = UserFb.objects.get(user=user_dj)
            data = {'userinfo': user_fb}
            return render(request, 'gettoken/index.html', data)
        else:
            return render(request, 'gettoken/login.html')
    else:
        if request.user.is_authenticated():
            user_dj = UserDj.objects.get(pk=request.user.pk)
            user_fb = UserFb.objects.get(user=user_dj)
            data = {'userinfo': user_fb}
            return render(request, 'gettoken/index.html', data)
        else:
            data = request.POST
            name = data['user_name']
            password = data['password']
            user_now = authenticate(username=name, password=password)
            if user_now is not None:
                if user_now.is_active:
                    login(request, user_now)
                    school = School()
                    school.save()
                    location = Location()
                    location.save()
                    token = TokenInfo()
                    token.save()
                    user_fb = UserFb()
                    user_fb.fb_education = school
                    user_fb.fb_location = location
                    user_fb.fb_token = token
                    user_fb.user = user_now
                    user_fb.save()
                    return render_to_response('gettoken/index.html', data)
                else:
                    return HttpResponse("Usuario no activado")
            else:
                return HttpResponse("Ingrese sus datos correctos")


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


def getaccess(request):
    redir = "http://locales.code.bo/"
    urls = "https://www.facebook.com/dialog/oauth?+client_id="
    urls += fb_app_id+"&response_type=token"+"&redirect_uri="+redir
    urls += scope
    # render_to_response("foo.html", RequestContext(request, {}))
    # res = HttpResponseRedirect(urls,request)
    res = redirect(urls, request)
    return res


def savetoken(request, youtoken, youexpires):
    print "savetoken"
    user_dj = UserDj.objects.get(pk=request.user.pk)
    user_fb = UserFb.objects.get(user=user_dj)
    token = TokenInfo()
    token.token = youtoken
    token.expires = youexpires
    token.save()
    token_del = TokenInfo.objects.get(pk=user_fb.fb_token.pk)
    token_del.delete()
    user_fb.fb_token = token
    user_fb.save()
    print user_fb.fb_token.token
    print user_fb.fb_token.expires
    return HttpResponseRedirect("http://locales.code.bo/")


def update(request):
    user_dj = UserDj.objects.get(pk=request.user.pk)
    user_fb = UserFb.objects.get(user=user_dj)
    token = user_fb.fb_token.token
    graph = facebook.GraphAPI(access_token=token, version='2.7')
    scope = "id,name,first_name,last_name,email,birthday,education,location"
    profile = graph.get_object(id='me', fields=scope)
    location = Location()
    if Location.objects.filter(location_id=profile["location"]["id"]).exists():
        location = Location.objects.get(location_id=profile["location"]["id"])
    location.location_id = profile["location"]["id"]
    location.location_name = profile["location"]["name"]
    location.save()

    user = user_fb
    user.fb_id = profile["id"]
    user.fb_first_name = profile["first_name"]
    user.fb_last_name = profile["last_name"]
    user.fb_email = profile["email"]
    user.fb_birthday = parser.parse(profile["birthday"]).date()
    user.fb_name = profile["name"]
    user.fb_location = location
    if profile.has_key("education"):
        user.fb_education = user.setEducation(profile["education"])
    user.save()
    return HttpResponseRedirect("http://locales.code.bo/token/")
