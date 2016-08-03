from django.shortcuts import render
from django.http import HttpResponseRedirect


def index_view(request):
    fb_app_id = 'you_id_app'
    if request.method == 'GET':
        return render(request, 'gettoken/index.html')
    elif request.method == 'POST':
        redir = "http://locales.code.bo/token/"
        urls = "https://www.facebook.com/dialog/oauth?+client_id="
        urls += fb_app_id+"&response_type=token"+"&redirect_uri="+redir
        res = HttpResponseRedirect(urls)
        return res


def savetoken(request, token):
    return HttpResponseRedirect("http://locales.code.bo/token/")
