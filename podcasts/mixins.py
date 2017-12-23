from django.conf import settings
from django.contrib.auth.models import User
from .models import *
from .forms import *

class LookupUserMixin(object):
    """
    Mixin to enable "Search for a friend" functionality in sidebar.
    """

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context.
        # Add additional context to be passed through to the template.
        # Use 'super' on the Mixin itself to function with multiple Classes simultaneously.
        context = super(LookupUserMixin, self).get_context_data(**kwargs)
        context['flag'] = 0
        searchterm = self.request.GET.get("q")
        result = User.objects.filter(username__iexact=searchterm)
        print(self.request.user.pk)
        if (searchterm and not result):
            context['flag'] = 1
            pk = self.request.user.pk
        elif (result):
            pk = result[0].pk
        else:
            pk = self.request.user.pk
        context['owner'] = User.objects.get(pk=pk)
        return context
