from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from gettoken import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^savetoken/(?P<youtoken>\w+)/(?P<youexpires>\w+)/$',
        views.savetoken, name='savetoken'),
    # url(r'^token/', include('gettoken.urls')),
    # url(r'^login/', views.loginuser, name='loginuser'),
    # url(r'^getaccess/', views.getaccess, name='access'),
    # url(r'^$', views.index, name='index'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
