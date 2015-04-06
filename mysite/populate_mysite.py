import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()



from polls.models import Category, Question, Choice

import datetime 
def populate():
    cat = add_cat("Science")
    question_pub_date = datetime.datetime.strptime("2011-10-01 15:26", "%Y-%m-%d %H:%M") 
    science_question =  add_question(cat, "What is the shape of the Earth", question_pub_date, 1)

    add_choice(science_question, "Oval Shape", 100)

    for c in Category.objects.all(): 
        for q in Question.objects.filter(category = c):
            for ch in Choice.objects.filter(question  = q):
                print "- {0} - {1} - {2}".format(str(c), str(q), str(ch))

def add_choice(question, choice_txt, votes = 0):
    c = Choice.objects.get_or_create(question=question, choice_text = choice_txt)[0]
    c.votes = votes
    c.save()
    return c

def add_question(cat, quest_txt, date, likes = 0):
    q = Question.objects.get_or_create(category=cat, question_text=quest_txt, pub_date= date, likes = likes)[0]
    return q

def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    return c

#Start execution here!
if __name__ == '__main__':
    print "Starting mysite population script..."
    populate()
