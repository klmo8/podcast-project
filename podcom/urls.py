"""podcom URL Configuration

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
from django.contrib import admin
from podcasts.views import *
from django.views.generic import View, TemplateView, DetailView, ListView, CreateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # "as_view()" is a method that creates an instance of this class
    url(r'^podcom/$', PodcastListView.as_view(), name='dashboard'),
    url(r'^podcom/details/(?P<pk>\d+)/', PodcastDetailView.as_view(template_name='detailpod.html')),
    url(r'^podcom/add/$', PodcastAddView.as_view()),
    url(r'^podcom/delete/$', TemplateView.as_view(template_name='deletepod.html')),
    url(r'^podcom/details/edit/(?P<pk>\d+)/$', PodcastUpdateView.as_view()),
    url(r'^podcom/mycom/$', TemplateView.as_view(template_name='friends.html')),
    url(r'^podcom/mycom/viewfriend/$', TemplateView.as_view(template_name='friendpage.html')),
    url(r'^podcom/mycom/add/$', TemplateView.as_view(template_name='addfriend.html')),
    url(r'^podcom/mycom/delete/$', TemplateView.as_view(template_name='deletefriend.html')),
    url(r'^podcom/mycom/details/$', TemplateView.as_view(template_name='fdetailpod.html')),
]
