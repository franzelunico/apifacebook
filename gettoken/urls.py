from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
        'gettoken.views',
        url(r'^$', views.index_view, name='index'),
)
