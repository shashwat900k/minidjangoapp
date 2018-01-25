"""thesocialnetwork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from . import views as view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^notifications/', include('notify.urls', namespace='notifications')),
    url(r'^login/$', views.login, name='login'),
    url(r'^signup/$', view.signup, name='signup'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^about/$', view.profile, name='profile'),
    url(r'^update_info/$', view.update_profile, name='update_profile'),
    url(r'search/(?P<data>.*)', view.search_users, name='search'),
    url(r'send_request/(?P<data>.*)', view.send_request, name='send_request'),
    url(r'^user/(?P<data>.*)', view.fetch_particular_user, name='particular_user'),
    url(r'^$', view.home, name='home'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
