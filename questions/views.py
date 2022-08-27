from django.core.paginator import Paginator

from django.contrib import messages

from django.db.models import Q

from django.http import HttpResponse

from django.shortcuts import render, redirect

from helpers.decorators import *
from helpers.views import *

from questions.filters import *
from questions.models import *
from questions.forms import *

from authentication.models import *


def HomePageView(request, *args, **kwargs):
    client_ip = get_client_ip(request)

    try:
        User.objects.get(email='botty@community.com', username='Community Bot')
    except User.DoesNotExist:
        User.objects.create_bot(email='botty@community.com', username='Community Bot')

    try:
        UserProfile.objects.get(first_name='Bot', last_name='👾')
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=User.objects.get(email='botty@community.com', username='Community Bot'),
                                   first_name='Bot', last_name='👾', birthdate=timezone.now(), gender='B',
                                   bio="I am a bot...👾")

    tags = Tag.objects.all()
    questions = Question.objects.all()
    users = User.objects.all()
    userprofiles = UserProfile.objects.all()

    total_posts = Question.objects.count()

    pagination = Paginator(questions, 10)
    page_number = request.GET.get('page')

    questions = pagination.get_page(page_number)

    context = {
        'tags': tags,
        'questions': questions,
        'users': users,
        'userprofiles': userprofiles,
        'total_posts': total_posts,
    }
    return render(request, 'questions/index.html', context)


def QuestionView(request, *args, **kwargs):
    client_ip = get_client_ip(request)

    slug = kwargs['slug']
    question_id = kwargs['question_id']

    request.session[f'viewed_post_{question_id}_by_{client_ip}'] = False

    try:
        question = Question.objects.get(slug=slug, pk=question_id)
        request.session[f'viewed_post_{question.id}_by_{client_ip}'] = True

        tracked_post, created = TrackedPost.objects.get_or_create(question=question,
                                                                  ip=client_ip)  # note, not actual api
        if created:
            tracked_post.view_count += 1
            tracked_post.save()

        post_count = TrackedPost.objects.filter(question=question).count()

    except Question.DoesNotExist:
        return HttpResponse('There is no such question')

    form = AnswerForm()

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():

            if request.user.userprofile.first_name == None:
                messages.warning(request, 'You need to create a profile before you can do that😣!')
                return redirect(f'/user/{request.user.slug}/{request.user.pk}/edit/?next={request.path}')

            Answer.objects.create(question=question, answerer=request.user.userprofile, **form.cleaned_data)
            return redirect('questions:question', question_id=question_id, slug=slug)

    context = {
        'question': question,
        'question_view_count': post_count,
        'answers_count': question.answers.count(),
        'now': timezone.now(),
        'form': form
    }
    return render(request, 'questions/question_view.html', context)


@redirect_unauthenticated_user_to_signin(login_url='authentication:signin')
def AskQuestion(request, *args, **kwargs):
    client_ip = get_client_ip(request)

    try:
        request.user.userprofile.first_name
    except User.userprofile.RelatedObjectDoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    if request.user.userprofile.first_name == None:
        messages.warning(request, 'You need to create a profile before you can ask a question😣!')
        return redirect(f'/user/{request.user.slug}/{request.user.pk}/?next={request.path}')

    form = AskQuestionForm()

    if request.method == 'POST':
        form = AskQuestionForm(request.POST)

        try:
            question = Question.objects.get(question=form.data['question'], title=form.data['title'],
                                            questioner=request.user.userprofile)
            if question:
                messages.error(request, f'You have already asked this question🤨')
            return redirect('questions:question', slug=question.slug, question_id=question.pk)

        except Question.DoesNotExist:
            if form.is_valid():
                messages.success(request, 'Question asked✔')
                question = Question.objects.create(questioner=request.user.userprofile, **form.cleaned_data)
            return redirect('questions:question', question.pk, question.slug)

    context = {
        'form': form,
    }

    return render(request, 'questions/ask_question.html', context)


def SearchResults(request, *args, **kwargs):
    client_ip = get_client_ip(request)

    # destination = request.POST.get('next')

    #     if destination:
    #         return redirect (destination)

    print(request.POST)

    if len(request.GET.get('x')) == 0:
        messages.warning(request, "You did not input a search value😒!")
        return redirect('questions:home')
    else:
        pass

    if request.method == 'GET':
        query = request.GET.get('x')

        search_results = Q(
            Q(title__istartswith=query) |
            Q(tag__name__iexact=query) |
            Q(questioner__first_name__exact=query) |
            Q(questioner__user__username__exact=query)
        )

        user_search_results = Q(
            Q(first_name__exact=query) |
            Q(last_name__exact=query)
        )

        results = Question.objects.filter(search_results)
        user_results = UserProfile.objects.filter(user_search_results)

    context = {
        'questions': results,
        'users': user_results,
    }

    return render(request, 'questions/search_results.html', context)
