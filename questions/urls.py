from django.urls import path

from questions.views import *

app_name = 'questions'
urlpatterns = [
    path('', HomePageView, name='home'),
    path('ask/', AskQuestion, name='ask'),
    path('<int:question_id>/<slug:slug>/', QuestionView, name='question'),
    path('result/', SearchResults, name='search_results'),
]