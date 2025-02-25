from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse

# Create your views here.

class HomeView(View):
    
    def get(self, request):
        #return HttpResponse("This will be the landing page.")
        return render(request, "home.html")