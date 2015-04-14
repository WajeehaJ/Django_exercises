from django.shortcuts import render
from django.http import HttpResponse
from polls.models import Question, Category
from polls.forms import QuestionForm, CategoryForm
from django.template import RequestContext
from django.shortcuts import render_to_response
from polls.forms import UserForm, UserProfileForm
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()

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
    #request.session.set_test_cookie()
    #context_dict = {'boldmessage' : "I'm bold font from the context"}
    category_list = Category.objects.order_by('-slug')[:5]
    context_dict = {'categories': category_list}
    #storing session data on server side
    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False
    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        if (datetime.now() - last_visit_time).seconds > 0:
            visits = visits + 1 
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True
    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits']  = visits
    context_dict['visits'] = visits
                 
    return render(request, 'polls/index.html', context_dict)
    
    #return HttpResponse("Hello, world. <br/> <a href='/polls/about'>About Poll page</a>")

#create a view name about for the poll administration page
def about(request):

     return render(request, 'polls/about.html', '')
#    return HttpResponse("You are at the poll about page")

def register(request):
    if request.session.test_cookie_worked():
        print ">>>> TEST COOKIE WORKED!"
        request.session.delete_test_cookie()
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print user_form.errors, profile_form.errors
          
    else: 
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'polls/register.html', {'user_form': user_form, 
                  'profile_form': profile_form, 'registered': registered} )

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/polls/')
            else:
                return HttpResponse("Your My Site  account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'polls/login.html', {})
