from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from .models import Podcast
from .forms import PodcastAddForm, PodcastUpdateForm


class DashboardView(TemplateView):
    # Adding args and kwargs to the get call allows us to print, modify, work with the arguments that are passed through the URL.
    # Example: PodCom/MyCom/<userID> and we can now access <userID> directly.
    # def get(self, request, *args, **kwargs):
    #     context = {}
    #     return render(request, "dashboard.html", {})
    template_name = 'dashboard.html'

    def get_context_data(self, *args, **kwargs):
        # Gets the context that is being passed by default to this view.
        context = super(DashboardView, self).get_context_data(*args, **kwargs)
        print(context)
        return context

class PodcastListView(ListView):
    template_name = 'dashboard.html'

    def get_queryset(self):
        queryset = Podcast.objects.all()
        print(self.kwargs)
        return queryset

class PodcastDetailView(DetailView):
    template_name = 'detailpod.html'

    # This is required because it is only with this queryset that we can get the appropriate context_data using the method below
    # It seems like it needs the queryset to match the context_data to grab
    queryset = Podcast.objects.all()

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        obj = get_object_or_404(Podcast, id=pk)
        return obj

class PodcastAddView(CreateView):
    form_class = PodcastAddForm
    template_name = 'addpod.html'
    success_url = '/podcom/'

class PodcastUpdateView(UpdateView):
    form_class = PodcastUpdateForm
    template_name = 'editpod.html'
    success_url = '/podcom/'

    queryset = Podcast.objects.all()
