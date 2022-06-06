from django.db import models

from django.urls import reverse
from django.template.defaultfilters import slugify

from users.models import *
from helpers.models import *


def bot():
    return UserProfile.objects.get(first_name='Bot', last_name='👾').pk


class Tag(TrackingModel):
    name = models.CharField(max_length=70, null=True)

    def __str__(self):
        return f'{ self.name }'


class Question(TrackingModel):
    questioner = models.ForeignKey(UserProfile, related_name='questions', on_delete=models.SET_DEFAULT, default=bot)
    title = models.CharField(max_length=200, null=True)
    slug = models.SlugField()
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
    question = models.TextField()
    date_asked = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{ self.title }'

    def get_absolute_url(self):
        return reverse('questions:question', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): 
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
class Answer(TrackingModel):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    answerer = models.ForeignKey(UserProfile, related_name='answers_given', on_delete=models.SET_DEFAULT, default=bot)
    answer = models.TextField()

    def __str__(self):
        return f'{self.question.title}'

class TrackedPost(TrackingModel):
    question = models.ForeignKey(Question, related_name='tracker', on_delete=models.CASCADE)
    ip = models.CharField(max_length=16) #only accounting for ipv4
    view_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{ self.ip } viewed question { self.question.pk }'

# ToDo: Modify this model and create a default userprofile and tag so that once someone deletes their profile, the default userprofile would claim the question. 
# ToDo: I just discovered i need a bot system in this app when it gets bigger.