from django.http import HttpResponse
from django.shortcuts import render

def renderTestGrid(request):
	return render(request, "index.html")

def renderConfigPage(request):
	return render(request, "savepref.html")
