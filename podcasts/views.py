from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import *
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Workaround to redirect users to their personal dashboard after successfully logging in.
@login_required
def home(request):
    return HttpResponseRedirect(reverse('dashboard_with_pk', args=[request.user.pk]))

class RegisterView(CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    success_url = '/podcom/'

class PodcastListViewPK(LoginRequiredMixin, ListView):
    template_name = 'podcasts/dashboard_with_pk.html'
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        queryset = Podcast.objects.filter(user=pk)
        return queryset

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context.
        context = super(PodcastListViewPK, self).get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        # Add additional context to be passed through to the template.
        context['owner'] = User.objects.get(pk=pk)
        return context


class PodcastListView(LoginRequiredMixin, ListView):
    template_name = 'podcasts/dashboard.html'
    redirect_field_name = 'redirect_to'


    def get_queryset(self):
        queryset = Podcast.objects.filter(user=self.request.user)
        return queryset

class PodcastDetailView(LoginRequiredMixin, DetailView):
    template_name = 'podcasts/detailpod.html'

    # This is required because it is only with this queryset that we can get the appropriate context_data using the method below
    # ?????????? queryset = Podcast.objects.all()

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        # Need to check if self.request.user is == obj.user
        obj = get_object_or_404(Podcast, id=pk)
        # if obj.user == self.request.user:
        return obj

class PodcastAddView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    form_class = PodcastAddForm
    template_name = 'podcasts/addpod.html'

    def get_success_url(self):
        return reverse('dashboard_with_pk', args=(self.request.pk,))


    # Saves the valid form with the current user being associated with the saved form data.
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        return super(PodcastAddView, self).form_valid(form)

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

    # saves the valid form with the current user being associated with the saved form data
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        return super(PodcastUpdateView, self).form_valid(form)

class PodcastDeleteView(LoginRequiredMixin, DeleteView):
    form_class = PodcastDeleteForm
    template_name = 'podcasts/deletepod.html'
    success_url = '/podcom/'

    queryset = Podcast.objects.all()

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        return super(PodcastDeleteView, self).form_valid(form)

class UserListView(LoginRequiredMixin, ListView):
    template_name = 'podcasts/users.html'

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset
