from django.shortcuts import render
from django.http import HttpResponse
from polls.models import Question

def index(request):
    #context_dict = {'boldmessage' : "I'm bold font from the context"}
    question_list = Question.objects.order_by('-likes')[:2]
    context_dict = {'Questions': question_list}
    return render(request, 'polls/index.html', context_dict)
    
    #return HttpResponse("Hello, world. <br/> <a href='/polls/about'>About Poll page</a>")

#create a view name about for the poll administration page
def about(request):

     return render(request, 'polls/about.html', '')
#    return HttpResponse("You are at the poll about page")

