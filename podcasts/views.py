from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import *
from .forms import *
from .mixins import *
import requests


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
        user_pk = self.request.user.pk
        searchterm = self.request.GET.get("q")
        result = User.objects.filter(username__iexact=searchterm)
        if (result):
            pk = result[0].pk
        else:
            pk = self.kwargs.get("pk")
        queryset = Podcast.objects.filter(user=pk)
        pk = int(pk)
        user_pk = int(user_pk)
        if not queryset and pk == user_pk:
            queryset = Podcast.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context.
        # Add additional context to be passed through to the template.
        context = super(PodcastListViewPK, self).get_context_data(**kwargs)
        context['flag'] = False
        searchterm = self.request.GET.get("q")
        result = User.objects.filter(username__iexact=searchterm)
        if (searchterm and not result):
            context['flag'] = True
            pk = self.kwargs.get("pk")
        elif (result):
            pk = result[0].pk
        else:
            pk = self.kwargs.get("pk")
        context['owner'] = User.objects.get(pk=pk)

        # Set flag for new user if no podcasts associated with user
        podcasts = Podcast.objects.filter(user=self.request.user.pk)
        if not podcasts:
            context['is_podcasts'] = False
        else:
            context['is_podcasts'] = True

        # Get friendslist to determine whether or not to display 'Add user to Friendslist' button
        try:
            friend = Friend.objects.get(current_user=self.request.user.pk)
            friends = friend.users.all()
            context['is_friend'] = False
            for friend in friends:
                if friend == User.objects.get(pk=pk):
                    context['is_friend'] = True
        except Friend.DoesNotExist:
            pass

        return context


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
        # Get podcast title to make API call with
        url = "https://itunes.apple.com/search?media=podcast&limit=1&term={}"
        title = self.request.POST.get("title")
        r = requests.get(url.format(title)).json()
        if r["resultCount"] > 0:
            # Set the retrieved artwork as the artwork for the newly added podcast
            artworkUrl = (r["results"][0]["artworkUrl600"])
            form.instance.logo = artworkUrl

        instance = form.save(commit=False)
        instance.user = self.request.user
        return super(PodcastAddView, self).form_valid(form)


# FBV to add functionality for an "Add this Podcast" button
def add_this_podcast(request, *args, **kwargs):

    # Get the pk of the podcast to be added (passed via kwargs) and then get that object from the Model
    pk = kwargs.get('pk')
    obj = get_object_or_404(Podcast, id=pk)

    # Check if podcast already exists in this user's database
    exists = Podcast.objects.filter(user=request.user, title=obj.title)
    if (exists):
        messages.error(
            request, 'The selected podcast was not added because it already exists in your list')
    else:
        messages.success(request, 'Podcast successfully added')
        # Save relevant information retrieved from model to current user
        podcast = Podcast.objects.create(
            user=request.user, title=obj.title, description=obj.description, url=obj.url, logo=obj.logo)
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
        context = super(PodcastUpdateView, self).get_context_data(
            *args, **kwargs)
        return context

    def get_object(self, *args, **kwargs):
        obj = super(PodcastUpdateView, self).get_object(*args, **kwargs)
        if obj.user != self.request.user:
            raise PermissionDenied()  # or Http404
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


# Credit to Max Goodridge (https://www.youtube.com/watch?v=Fc2O3_2kax8&list=PLw02n0FEB3E3VSHjyYMcFadtQORvl1Ssj).
# The below code for friendships was adapted from his Django tutorial series.
def update_friends(request, operation, pk):

    friend = User.objects.get(pk=pk)

    if operation == 'add':
        # Get user by pk to add this user to current user's list of friends
        Friend.make_friend(request.user, friend)
        messages.success(request, 'User successfully added to Friendlist')

    elif operation == 'remove':
        Friend.unfriend(request.user, friend)
        messages.success(request, 'User successfully removed from Friendlist')

    return HttpResponseRedirect(reverse('friendlist', args=[request.user.pk]))


class FriendListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    template_name = 'podcasts/friendlist.html'

    def get_queryset(self):
        try:
            friend = Friend.objects.get(current_user=self.request.user)
            queryset = friend.users.all()
            return queryset
        except Friend.DoesNotExist:
            pass

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context.
        # Add additional context to be passed through to the template.
        context = super(FriendListView, self).get_context_data(**kwargs)
        context['flag'] = False
        try:
            friend = Friend.objects.get(current_user=self.request.user)
            queryset = friend.users.all()
            if queryset:
                context['flag'] = True
            return context
        except Friend.DoesNotExist:
            pass
