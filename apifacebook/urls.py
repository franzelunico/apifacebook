from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from gettoken import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.loginuser, name='loginuser'),
    url(r'^savetoken/(?P<youtoken>\w+)/(?P<youexpires>\w+)/$',
        views.savetoken, name='savetoken'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
