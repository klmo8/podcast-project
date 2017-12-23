from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import *
from .forms import *
from .mixins import *


# Workaround to redirect users to their personal dashboard after successfully logging in.
@login_required
def home(request):
    return HttpResponseRedirect(reverse('dashboard_with_pk', args=[request.user.pk]))

class RegisterView(CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    success_url = '/podcom/'


class PodcastListViewPK(LoginRequiredMixin, LookupUserMixin, ListView):
    template_name = 'podcasts/dashboard_with_pk.html'
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        searchterm = self.request.GET.get("q")
        result = User.objects.filter(username__iexact=searchterm)
        if (result):
            pk = result[0].pk
        else:
            pk = self.kwargs.get("pk")
        queryset = Podcast.objects.filter(user=pk)
        return queryset

class PodcastListView(LoginRequiredMixin, ListView):
    template_name = 'podcasts/dashboard.html'
    redirect_field_name = 'redirect_to'


    def get_queryset(self):
        queryset = Podcast.objects.filter(user=self.request.user)
        return queryset


class PodcastDetailView(LoginRequiredMixin, DetailView):
    template_name = 'podcasts/detailpod.html'

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        obj = get_object_or_404(Podcast, id=pk)
        return obj


class PodcastAddView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    success_url = '/podcom/'
    form_class = PodcastAddForm
    template_name = 'podcasts/addpod.html'
    success_message = "Podcast successfully added"

    # Saves the valid form with the current user being associated with the saved form data.
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        return super(PodcastAddView, self).form_valid(form)


# FBV to add functionality for an "Add this Podcast" button
def add_this_podcast(request, *args, **kwargs):

    # Get the pk of the podcast to be added (passed via kwargs) and then get that object from the Model
    user_pk = request.user.pk
    pk = kwargs.get('pk')
    obj = get_object_or_404(Podcast, id=pk)

    # Check if podcast already exists in this user's database
    exists = Podcast.objects.filter(user=request.user, title=obj.title)
    if (exists):
        messages.error(request, 'The selected podcast was not added because it already exists in your list')
    else:
        messages.success(request, 'Podcast successfully added')
        # Save relevant information retrieved from model to current user
        podcast = Podcast.objects.create(user=request.user, title=obj.title, description=obj.description, url=obj.url, logo=obj.logo)
        podcast.save()
    # Redirect to dashboard
    return HttpResponseRedirect(reverse('dashboard_with_pk', args=[request.user.pk]))

class PodcastUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PodcastUpdateForm
    template_name = 'podcasts/editpod.html'
    success_url = '/podcom/'

    queryset = Podcast.objects.all()

    def get_context_data(self, *args, **kwargs):
        # Gets the context that is being passed by default to this view.
        context = super(PodcastUpdateView, self).get_context_data(*args, **kwargs)
        return context

    def get_object(self, *args, **kwargs):
        obj = super(PodcastUpdateView, self).get_object(*args, **kwargs)
        if obj.user != self.request.user:
            raise PermissionDenied() #or Http404
        return obj

    # Saves the valid form with the current user being associated with the saved form data
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        return super(PodcastUpdateView, self).form_valid(form)

class PodcastDeleteView(LoginRequiredMixin, DeleteView):
    form_class = PodcastDeleteForm
    template_name = 'podcasts/deletepod.html'
    success_url = '/podcom/'
    success_message = "Podcast successfully deleted"

    queryset = Podcast.objects.all()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PodcastDeleteView, self).delete(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        return super(PodcastDeleteView, self).form_valid(form)

class UserListView(LoginRequiredMixin, LookupUserMixin, ListView):
    template_name = 'podcasts/users.html'

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset
