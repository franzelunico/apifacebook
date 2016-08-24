from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from gettoken import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^token/', include('gettoken.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^getaccess/', views.getaccess, name='access'),
    url(r'^update/', views.update, name='update'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
