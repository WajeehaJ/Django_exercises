import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()



from polls.models import Question, Choice

import datetime 
def populate():
    question_pub_date = datetime.datetime.strptime("2011-10-01 15:26", "%Y-%m-%d %H:%M") 
    science_question =  add_question("What is the shape of the Earth", question_pub_date, 1)

    add_choice(science_question, "Oval Shape", 100)

    for q in Question.objects.all():
        for c in Choice.objects.filter(question  = q):
            print "- {0} - {1}".format(str(q), str(c))

def add_choice(question, choice_txt, votes = 0):
    c = Choice.objects.get_or_create(question=question, choice_text = choice_txt)[0]
    c.votes = votes
    c.save()
    return c

def add_question(quest_txt, date, likes = 0):
    q = Question.objects.get_or_create(question_text=quest_txt, pub_date= date, likes = likes)[0]
    return q


#Start execution here!
if __name__ == '__main__':
    print "Starting mysite population script..."
    populate()
