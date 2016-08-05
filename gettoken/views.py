import urllib
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import TokenInfo, User
import ast


fb_app_id = 'you_id'


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
    url = 'https://graph.facebook.com/me/?access_token='
    url += youtoken
    resp = urllib.urlopen(url)
    if resp.getcode() == 200:
        readed = resp.read()
        readed = ast.literal_eval(readed)
        user = User()
        user.fb_name = readed.get("name")
        user.fb_id = readed.get("id")
        if User.objects.all().filter(fb_id=user.fb_id).count() == 0:
            user.save()
            tokeninfo = TokenInfo()
            tokeninfo.token = youtoken
            tokeninfo.expires = youexpires
            tokeninfo.save()

    return HttpResponseRedirect("http://locales.code.bo/token/")
