from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import *

class RegisterView(CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    #TODO: redirect to homepage instead, then send user confirmation email.
    success_url = '/podcom/'

# Not currently being routed (see PodcastListView instead).
class DashboardView(TemplateView):
    # Adding args and kwargs to the get call allows us to print, modify, work with the arguments that are passed through the URL.
    # Example: PodCom/MyCom/<userID> and we can now access <userID> directly.
    # def get(self, request, *args, **kwargs):
    #     context = {}
    #     return render(request, "dashboard.html", {})
    template_name = 'podcasts/dashboard.html'

    def get_context_data(self, *args, **kwargs):
        # Gets the context that is being passed by default to this view.
        context = super(DashboardView, self).get_context_data(*args, **kwargs)
        print(context)
        return context

class PodcastListViewPK(LoginRequiredMixin, ListView):
    template_name = 'podcasts/dashboard_with_pk.html'
    redirect_field_name = 'redirect_to'


    def get_queryset(self):
        pk = self.kwargs.get("pk")
        queryset = Podcast.objects.filter(user=pk)
        return queryset

class PodcastListView(LoginRequiredMixin, ListView):
    template_name = 'podcasts/dashboard.html'
    redirect_field_name = 'redirect_to'


    def get_queryset(self):
        # print(self.request.user)
        # queryset = Podcast.objects.all()
        queryset = Podcast.objects.filter(user=self.request.user)
        print(self.kwargs)
        return queryset

class PodcastDetailView(LoginRequiredMixin, DetailView):
    template_name = 'podcasts/detailpod.html'

    # This is required because it is only with this queryset that we can get the appropriate context_data using the method below
    # It seems like it needs the queryset to match the context_data to grab
    queryset = Podcast.objects.all()

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        obj = get_object_or_404(Podcast, id=pk)
        return obj

class PodcastAddView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    form_class = PodcastAddForm
    template_name = 'podcasts/addpod.html'
    success_url = '/podcom/'


    # Saves the valid form with the current user being associated with the saved form data.
    def form_valid(self, form):
        instance = form.save(commit=False)
        #LoginRequiredMixin ensures that this is a valid/logged-in user.
        instance.user = self.request.user
        return super(PodcastAddView, self).form_valid(form)

class PodcastUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PodcastUpdateForm
    template_name = 'podcasts/editpod.html'
    success_url = '/podcom/'

    queryset = Podcast.objects.all()

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

    # saves the valid form with the current user being associated with the saved form data
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        return super(PodcastDeleteView, self).form_valid(form)

class UserListView(LoginRequiredMixin, ListView):
    template_name = 'podcasts/users.html'

    def get_queryset(self):
        queryset = User.objects.all()
        # queryset = class_instance.model_set.all()
        for query in queryset:
            print(query)
        return queryset


# class LoginView(LoginView):
#     redirect_authenticated_user = True
#     redirect_field_name = '/podcom/'
