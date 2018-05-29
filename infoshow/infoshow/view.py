from django.http import HttpResponse
from django.shortcuts import render
 
def index(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'index.html', context)
def search(request):
    search=request.GET['search']
    return HttpResponse('1')