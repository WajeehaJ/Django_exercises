from django.contrib import admin
from polls.models import Question, Choice, Category
from polls.models import UserProfile

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
    list_display = ('question_text','category', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date'] 
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

#admin.site.register(Question, QuestionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Question)
admin.site.register(UserProfile)
