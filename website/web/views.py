from .models import Post
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
import requests
from django.core.paginator import Paginator

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
            data = {}
            movies = {}

    return render(request, 'movie_finder.html', {"data": movie_list2,
        "movies": movies})
# Create your views here.
