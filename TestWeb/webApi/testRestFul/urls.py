from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # url(r'^testRestFul/$', views.snippet_list),
    # url(r'^testRestFul/(?P<pk>[0-9]+)/$', views.snippet_detail),

    url(r'^snippets/$', views.snippet_list),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
    url(r'^test_post', views.test_post),
    # url(r'^getlistpic', views.getlispic, name='home'),
    # url(r'^getlist', views.getlist, name='home'),
]

urlpatterns = format_suffix_patterns(urlpatterns)