from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse

import logging

# Create your views here.

class HomeView(View):

    
    def get(self, request):
        #return HttpResponse("This will be the landing page.")
        logger = logging.getLogger(__name__)
        logger.warning("very bad indeed")
        return render(request, "home.html")