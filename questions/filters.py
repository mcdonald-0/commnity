import django_filters
  
from . models import *

class QuestionFilter(django_filters.FilterSet):
	title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
	class Meta:
		model = Question
		fields = ['title',]


		#? download the word of jesus MP3 all of them