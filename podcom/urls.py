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
# from django.contrib.auth.views import LoginView
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from podcasts import views
from podcasts.views import *
from django.views.generic import View, TemplateView, DetailView, ListView, CreateView

urlpatterns = [
    # reverse_lazy tells the app to redirect to the page named 'login' after a user logs out.
    # as_view() is a method that creates an instance of this class.
    url(r'^podcom/$', home, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^podcom/(?P<pk>\d+)/$', PodcastListViewPK.as_view(), name='dashboard_with_pk'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^logout/$', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    url(r'^podcom/details/(?P<pk>\d+)/', PodcastDetailView.as_view(), name='details_with_pk'),
    url(r'^podcom/add/$', PodcastAddView.as_view(), name='addpodcast'),
    url(r'^podcom/add2/(?P<pk>\d+)/$', views.add_this_podcast, name='addthispodcast'),
    url(r'^podcom/delete/(?P<pk>\d+)/', PodcastDeleteView.as_view(), name='deletepodcast'),
    url(r'^podcom/details/edit/(?P<pk>\d+)/$', PodcastUpdateView.as_view(), name='editpodcast'),
    url(r'^podcom/users/$', UserListView.as_view(), name='userlist'),
    # url(r'^podcom/mycom/viewfriend/$', TemplateView.as_view(template_name='friendpage.html')),
    # url(r'^podcom/mycom/add/$', TemplateView.as_view(template_name='addfriend.html')),
    # url(r'^podcom/mycom/delete/$', TemplateView.as_view(template_name='deletefriend.html')),
    # url(r'^podcom/mycom/details/$', TemplateView.as_view(template_name='fdetailpod.html')),
]
