from django.contrib import admin
from polls.models import Question, Choice
st_display = ('question_text', 'pub_date', 'was_published_recently')
class ChoiceInline(admin.TabularInline): #admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    #fields = ['pub_date', 'question_text']
    fieldsets = [ 
        (None, { 'fields' : ['question_text']}),
        ('Date information', { 'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date'] 
# Register your models here.
admin.site.register(Question, QuestionAdmin)
