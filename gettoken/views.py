from django.shortcuts import render
from django.template import RequestContext
import urllib


def index_view(request):
    """docstring for index_view"""
    f_u = 'https://gist.github.com/aparrish/4683917#file-facebook_app_token-py'
    f_u = 'https://gist.github.com/dominicphillips/3124620#file-gistfile1-txt'
    f_u = 'https://graph.facebook.com/oauth/access_token?client_id='
    fb_app_id = 'asdf'
    fb_app_secret = 'asdf'
    resp = urllib.urlopen(f_u + fb_app_id + '&client_secret=' +
                          fb_app_secret + '&grant_type=client_credentials')
    return_if = ''
    if resp.getcode() == 200:
        return_if = resp.read().split("=")[1]
    else:
        return_if = None
    print return_if
    if request.method == 'GET':
        print 'metodo get'
        return render(request, 'gettoken/index.html')
    elif request.method == 'POST':
        print request.POST['user']
        print request.POST['token']
        print 'metodo post'
        return render(request, 'gettoken/index.html')
