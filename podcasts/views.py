from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView
from .models import Podcast


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

class PodcastList(ListView):
    template_name = 'dashboard.html'

    def get_queryset(self):
        queryset = Podcast.objects.all()
        print(self.kwargs)
        return queryset

class PodcastDetail(ListView):
    template_name = 'detailpod.html'

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        podcastQuery = Podcast.objects.get(title__iexact=slug)
        print(podcastQuery)
        return podcastQuery
