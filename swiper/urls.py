"""swiper URL Configuration

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
from django.conf.urls import url

from user import api as user_api
from social import api as social_api
from vip import api as vip_api


urlpatterns = [
    url(r'api/user/submit_phone', user_api.submit_phone),
    url(r'api/user/submit_vcode', user_api.submit_vcode),
    url(r'api/user/get_profile', user_api.get_profile),
    url(r'api/user/set_profile', user_api.set_profile),
    url(r'api/user/upload_avatar', user_api.upload_avatar),

    url(r'api/social/rcmd_users', social_api.rcmd_users),
    url(r'api/social/like', social_api.like),
    url(r'api/social/superlike', social_api.superlike),
    url(r'api/social/dislike', social_api.dislike),
    url(r'api/social/rewind', social_api.rewind),
    url(r'api/social/show_liked_me', social_api.show_liked_me),
    url(r'api/social/show_liked_me', social_api.show_liked_me),
    url(r'api/social/friends', social_api.friends),
    url(r'api/social/top10', social_api.top10),

    url(r'api/vip/show_vip', vip_api.show_vip),
]
