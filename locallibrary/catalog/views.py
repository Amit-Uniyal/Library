from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

# Create your views here.

def index(request):
	now = datetime.now()
	html = "<h2>It is now %s.</h2>"  % now.ctime()
	return HttpResponse(html)
  
