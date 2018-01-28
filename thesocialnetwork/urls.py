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
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import login, logout

from . import views

urlpatterns = [
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^login/$', login, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'profile/user/(?P<user_id>.*)', views.profile, name='particular_user'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^update_profile/$', views.update_profile, name='update_profile'),
    url(r'^write_something/', views.write_something, name='write_something'),
    url(r'search/(?P<data>.*)', views.search, name='search'),
    url(r'send_request/(?P<user_id>.*)', views.send_request, name='send_request'),
    url(r'user_reaction/(?P<data>.*)', views.user_reaction, name='user_reaction'),
    url(r'accept_request/(?P<request_id>.*)', views.accept_request, name='accept_request'),
    url(r'reject_request/(?P<request_id>.*)', views.reject_request, name='reject_request'),
    url(r'show_notifications', views.show_notifications, name='show_notifications'),
    url(r'^$', views.home, name='home'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
