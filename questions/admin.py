from django.contrib import admin

from questions.models import *

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)} 

admin.site.register(Tag)
admin.site.register(Question, QuestionAdmin)
admin.site.register(TrackedPost)
admin.site.register(Answer)



