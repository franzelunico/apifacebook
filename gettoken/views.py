from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from .models import Location, TokenInfo, User, School, Page
from django.http import HttpResponse
import facebook
from dateutil import parser
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
import json
from fabric.api import task
from fabric.operations import local
from time import gmtime, strftime


fb_app_id = '930344197111872'
redir = "http://local.fl.code.bo/"
scope = "&scope=user_about_me,email,user_birthday,user_education_history"
scope += ",user_location,user_likes"


@csrf_exempt
def index(request, *args, **kwargs):
    if request.method == 'GET':
        return render(request, 'gettoken/index.html')
    else:
        if request.method == 'POST':
            urls = "https://www.facebook.com/dialog/oauth?+client_id="
            urls += fb_app_id+"&response_type=token"+"&redirect_uri="+redir
            urls += scope
            res = redirect(urls, request)
            return res


def savetoken(request, youtoken, youexpires):
    graph = facebook.GraphAPI(access_token=youtoken, version='2.7')
    scope = "id,name,first_name,last_name,email,birthday,education,location"
    profile = graph.get_object(id='me', fields=scope)
    likes = graph.get_connections(id='me', connection_name='likes')
    namefile = profile["id"]
    namefile += "_me_"  # api
    # ISO 8601
    namefile += strftime("%Y-%m-%dT%H:%M:%S%z", gmtime())
    namefile += ".json"
    data = json.dumps(profile, indent=4)
    f = open(namefile, 'w')
    f.write(data)
    f.close()
    putfile(namefile)
    with open(namefile) as data_file:
        data = json.load(data_file)
        profile = data
    # database process
    user = getUser(profile, youtoken, youexpires)
    user.save()
    setWorkandEducation(profile, user)
    setPagesLikes(likes, user)
    return HttpResponseRedirect("/")


def getUser(profile, newtoken, token_expire):
    user = None
    token = None
    location = None
    if User.objects.filter(fb_id=profile["id"]).exists():
        user = User.objects.get(fb_id=profile["id"])
        user = setValuesUser(profile, user)
        token = user.fb_token
        token = setToken(newtoken, token_expire, token)
        location = setLocation(profile)
        user.fb_location = location
    else:
        user = User()
        setValuesUser(profile, user)
        token = TokenInfo()
        token = setToken(newtoken, token_expire, token)
        location = setLocation(profile)
    location.save()
    token.save()
    user.fb_token = token
    user.fb_location = location
    return user


def setValuesUser(profile, user):
    user.fb_id = profile["id"]
    user.fb_first_name = profile["first_name"]
    user.fb_last_name = profile["last_name"]
    user.fb_email = profile["email"]
    if "birthday" in profile:
        user.fb_birthday = parser.parse(profile["birthday"]).date()
    user.fb_name = profile["name"]
    return user


def setToken(newtoken, token_expire, token):
    token.token = newtoken
    token.expires = token_expire
    return token


def setLocation(profile):
    location = None
    if "location" in profile:
        loc_id = profile["location"]["id"]
        if Location.objects.filter(location_id=loc_id).exists():
            location = Location.objects.get(location_id=loc_id)
        else:
            location = Location()
            location.location_id = profile["location"]["id"]
            location.location_name = profile["location"]["name"]
    else:
        if Location.objects.filter(location_id="vacio").exists():
            location = Location.objects.get(location_id="vacio")
        else:
            location = Location()
    return location


def setWorkandEducation(profile, user):
    # no elimina los datos de usuario
    # for user_x in user.fb_highschool.all():
    #     user.fb_highschool.remove(user_x)
    if "education" in profile:
        for item in profile["education"]:
            if item['type'] == "High School":
                school = item['school']['id']
                if School.objects.filter(school_id=school).exists():
                    school = School.objects.get(school_id=school)
                else:
                    school = School()
                    school.school_id = item['school']['id']
                    school.school_name = item['school']['name']
                    school.save()
                user.fb_highschool.add(school)
    else:
        school = None
        if School.objects.filter(school_id="vacio").exists():
            school = School.objects.get(school_id="vacio")
        else:
            school = School()
            school.save()
        user.fb_highschool.add(school)


def setPagesLikes(likes, user):
    if "data" in likes:
        for item in likes["data"]:
                page = item['id']
                if Page.objects.filter(fb_id=page).exists():
                    page = Page.objects.get(fb_id=page)
                else:
                    page = Page()
                    page.fb_id = item['id']
                    page.name = item['name']
                    created_time = parser.parse(item["created_time"]).date()
                    page.created_time = created_time
                    page.save()
                user.fb_pages_likes.add(page)
    else:
        page = None
        if Page.objects.filter(fb_id="vacio").exists():
            page = Page.objects.get(fb_id="vacio")
        else:
            page = School()
            page.save()
        user.fb_pages_likes.add(page)


def my_custom_page_not_found_view(request):
    return render(request, 'gettoken/404.html')


def logoutnlogin(request):
    return logout_then_login(request, login_url='/login')


@task
def putfile(namefile):
    command = "aws s3 cp " + namefile + " s3://apifacebook/"
    local(command)


def loginuser(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            return HttpResponseRedirect("/useradmin/")
        else:
            return render(request, 'gettoken/login.html')
    else:
            data = request.POST
            name = data['user_name']
            password = data['password']
            user_now = authenticate(username=name, password=password)
            if user_now is not None:
                if user_now.is_active:
                    login(request, user_now)
                    return HttpResponseRedirect("/useradmin/")
                else:
                    return HttpResponse("Usuario no activado")
            else:
                return HttpResponse("Ingrese sus datos correctos")


@login_required(login_url='/login/')
def useradmin(request):
    user_fb = User.objects.all()
    data = {'userlist': user_fb}
    return render(request, 'gettoken/useradmin.html', data)
