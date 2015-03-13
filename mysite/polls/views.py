from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. <br/> <a href='/polls/about'>About Poll page</a>")

#create a view name about for the poll administration page
def about(request):
    return HttpResponse("You are at the poll about page")
