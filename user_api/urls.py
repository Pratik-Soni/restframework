'''
Created on 28-Jul-2016

@author: pratiksoni
'''
from django.conf.urls import url
from user_api import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
               #url(r'^userslist/$', views.user_list_old),
               #url(r'^users/(?P<pk>[0-9]+)/$', views.user_detail_old),
               #url(r'^userslist/$', views.users_list),
               #url(r'^users/(?P<pk>[0-9]+)/$', views.user_detail),
               url(r'^userslist/$', views.NewUsersList.as_view()),
               url(r'^user/(?P<pk>[0-9]+)/$', views.NewUserDetails.as_view()),
               url(r'^users/$', views.UserListO.as_view()),
               url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetailO.as_view()),
               ]

urlpatterns = format_suffix_patterns(urlpatterns)