import urllib
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import TokenInfo, User
import ast


fb_app_id = '930344197111872'


def index_view(request):
    if request.method == 'GET':
        return render(request, 'gettoken/index.html')
    elif request.method == 'POST':
        redir = "http://locales.code.bo/token/"
        urls = "https://www.facebook.com/dialog/oauth?+client_id="
        urls += fb_app_id+"&response_type=token"+"&redirect_uri="+redir
        res = HttpResponseRedirect(urls)
        return res


def savetoken(request, youtoken, youexpires):
    print youtoken
    consult = "?fields=id,name,picture,first_name,email"
    url = 'https://graph.facebook.com/me/'+consult+'/?access_token='
    url += youtoken
    print url
    resp = urllib.urlopen(url)
    if resp.getcode() == 200:
        print "get 200"
        readed = resp.read()
        print readed
    return HttpResponseRedirect("http://locales.code.bo/token/")
