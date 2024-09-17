from .models import Post, BlogPost
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
import requests
from django.core.paginator import Paginator
from html import unescape
from django.http import HttpResponseRedirect
import random
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm

def home(request):
    return render(request, 'home.html', {})

def github(request):
    return render(request, 'github_links.html', {})

def guest_book(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'guest_book.html', {'posts': posts})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.save()
            return redirect('guest_book')
    else:
        form = PostForm()
    return render(request, 'guest_book_entry.html', {'form': form})

def movie_finder(request):
    if request.method == 'POST':
        action = request.POST["submit"]
        movie_name = request.POST.get('movie')
        request.session['movie'] = movie_name

        url = f"https://api.themoviedb.org/3/search/movie?query={movie_name}&include_adult=false&language=en-US&page=1"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlNTI3YWQ0MzA2N2ZkY2JiYjZjZDE2ZWE4ZjA1ZWM2MCIsIm5iZiI6MTcyNTkyNjExOS42MjY3MDYsInN1YiI6IjY0YzNjYzNiZWMzNzBjMDEzOTY3OTkxZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.15QV1PIoF0aMedTp2BtRaDiffjh_dTyBESOTruUt8eQ"
        }

        response = requests.get(url, headers=headers)

        movie_list = response.json()

        data = movie_list["results"]

        movie_list2 = []
        for movie in data:
            string = str(movie["backdrop_path"])
            if string != "None":
                data1 = list(data)
                movie_list2.append(dict(movie))

        p = Paginator(movie_list2, 5)
        page = request.GET.get('page')
        movies = p.get_page(page)
        if action == "clear":
            request.session.pop('movie', None)

    if request.method == 'GET':
        if 'movie' in request.session:
            movie_name = request.session['movie']

            url = f"https://api.themoviedb.org/3/search/movie?query={movie_name}&include_adult=false&language=en-US&page=1"

            headers = {
                "accept": "application/json",
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlNTI3YWQ0MzA2N2ZkY2JiYjZjZDE2ZWE4ZjA1ZWM2MCIsIm5iZiI6MTcyNTkyNjExOS42MjY3MDYsInN1YiI6IjY0YzNjYzNiZWMzNzBjMDEzOTY3OTkxZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.15QV1PIoF0aMedTp2BtRaDiffjh_dTyBESOTruUt8eQ"
            }

            response = requests.get(url, headers=headers)

            movie_list = response.json()


            data = movie_list["results"]

            #takes all of the movie entries without pictures out
            movie_list2 = []
            for movie in data:
                string = str(movie["backdrop_path"])
                if string != "None":
                    data1 = list(data)
                    movie_list2.append(dict(movie))

            p = Paginator(movie_list2, 5)
            page = request.GET.get('page')
            movies = p.get_page(page)

        else:
            movie_list2 = {}
            movies = {}

    return render(request, 'movie_finder.html', {"data": movie_list2,
        "movies": movies})

def question_game(request):
    if request.method == 'POST':
        difficulty = request.POST.get('difficulty')
        category = request.POST.get('category')
        category_list = ['General', 'Entertainment: Books', 'Entertainment: Film', 'Entertainment: Music',
        'Entertainment: Video Games', 'Entertainment: Board Games', 'Science and Nature', 'Science: Computers'
        'Science: Mathematics', 'Mythology', 'Sports', 'Geography', 'History', 'Politics', 'Art', 'Celebrities',
        'Animals', 'Vehicles', 'Comics', 'Gadgets', 'Anime', 'Cartoons']

        cat_number = ""
        for cat in category_list:
            if cat == category:
                cat_number = category_list.index(cat) + 9

        difficulty = difficulty.lower()

        endpoint = f"https://opentdb.com/api.php?amount=20&category={cat_number}&difficulty={difficulty}&type=multiple"

        response = requests.get(endpoint)

        data = response.json()
        questions = data["results"]

        #unescape = HTMLParser().unescape
        #question_list = []
        #for question in questions:
        #    q = question['question']
        #    q = unescape(q)
        #    question_list.append(q)
        
        #answer_list = []
        #correct_answer_list = []
        #for answer in questions:
         #   a = answer["correct_answer"]
          #  answer_list.append(a)
           # correct_answer_list.append(a)
           # ia = answer["incorrect_answers"]
            #    for i in ia:
             #       answer_list.append(i)

        #random.shuffle(answer_list)



        request.session['questions'] = questions
        #return render(request, 'twenty_questions.html', {'question': question})
        return HttpResponseRedirect('twenty_questions')
    else:
        return render(request, 'question_game.html', {})

def twenty_questions(request):
    if request.method == 'POST':
        selection = request.POST.get('selection')
        number = request.session['number']
        if number == 19:
            counter = request.session['counter']
            return render(request, 'summary.html', {'counter': counter})

        questions = request.session["questions"]
        last_answer = questions[number]["correct_answer"]
        print(selection)
        print(last_answer)


        if selection == last_answer:
            request.session['counter'] += 1

        counter = request.session['counter']

        #below is for looping through the list of questions and getting the correct q/a's
        number = request.session['number']
        number += 1
        request.session['number'] = number
        #questions = request.session["questions"]
        question = questions[number]["question"]
        question = unescape(question)

        correct_answer = questions[number]["correct_answer"]
        correct_answer = str(unescape(correct_answer))
        request.session['correct_answer'] = correct_answer
        incorrect_answers = questions[number]["incorrect_answers"]
        answer_list = []
        for answer in incorrect_answers:
            answer = str(unescape(answer))
            answer_list.append(answer)
        answer_list.append(correct_answer)

        random.shuffle(answer_list)
        question_count = number + 1
        return render(request, 'twenty_questions.html', {'question': question,
            'answer_list': answer_list, 'counter': counter, 'question_count': question_count})
    if request.method == 'GET':
        questions = request.session['questions']
        number = 0
        request.session['number'] = number
        question = questions[number]["question"]
        question = unescape(question)


        correct_answer = questions[number]["correct_answer"]
        correct_answer = str(unescape(correct_answer))
        incorrect_answers = questions[number]["incorrect_answers"]
        answer_list = []
        for answer in incorrect_answers:
            answer = str(unescape(answer))
            answer_list.append(answer)
        answer_list.append(correct_answer)

        random.shuffle(answer_list)

        request.session['counter'] = 0

        question_count = number + 1

        return render(request, 'twenty_questions.html', {'question': question,
            'answer_list': answer_list, 'question_count': question_count})

def summary(request):
    counter = request.session['counter']
    return render(request, 'summary.html', {'counter': counter})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You are now logged in!"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error logging you in, check credentials"))
            return redirect('home')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out...Goodbye!"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(password)
            #login user
            user = form.save()
            #user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have successfully created an account!"))
            return redirect('home')
        else:
            messages.success(request, ("Oops! There was a problem registering your account."))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})


def blog(request):
    blog_posts = BlogPost.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    #reverse the list, makes it so newest post is first
    blog_posts = blog_posts[::-1]
    return render(request, 'blog.html', {'blog_posts': blog_posts})

def blog_post_detail(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog_post_detail.html', {'blog_post': blog_post})
