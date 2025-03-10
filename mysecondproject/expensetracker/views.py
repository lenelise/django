from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse

import logging

# Create your views here.


logger = logging.getLogger(__name__)

class HomeView(View):    
    def get(self, request):
        logger.debug("home.html rendered")
        return render(request, "home.html")