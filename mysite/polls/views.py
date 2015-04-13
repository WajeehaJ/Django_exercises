from django.shortcuts import render
from django.http import HttpResponse
from polls.models import Question, Category
from polls.forms import QuestionForm, CategoryForm
from django.template import RequestContext
from django.shortcuts import render_to_response


def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'polls/add_category.html', {'form': form})

def add_question(request, category_name_slug):
    context_dict = {}
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        return render(request, 'polls/add_category.html',  context_dict)
    if request.method  == 'POST':
        form  = QuestionForm(request.POST)
 
        if form.is_valid():
            question = form.save(commit=False)
            question.category = cat
            question.save()
            return category(request, category_name_slug)
        else: 
            print form.errors
    else:
        form = QuestionForm()
   
    context_dict = {'form': form, 'category': cat}
    return render(request, 'polls/add_question.html', context_dict)


def category(request, category_name_slug):  
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        questions = Question.objects.filter(category=category)

        context_dict['questions'] = questions
        context_dict['category'] = category
        context_dict['context_name_slug'] = category_name_slug
    except Category.DoesNotExist:
        pass

    return render(request, 'polls/category.html', context_dict)

def index(request):
    #context_dict = {'boldmessage' : "I'm bold font from the context"}
    category_list = Category.objects.order_by('-slug')[:5]
    context_dict = {'categories': category_list}
    return render(request, 'polls/index.html', context_dict)
    
    #return HttpResponse("Hello, world. <br/> <a href='/polls/about'>About Poll page</a>")

#create a view name about for the poll administration page
def about(request):

     return render(request, 'polls/about.html', '')
#    return HttpResponse("You are at the poll about page")

