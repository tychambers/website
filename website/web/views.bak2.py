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
    if request.GET.get('movie') == "None" or "none":
        data = {}
        movies = {}
    elif request.method == 'GET':
        movie_name = request.GET.get('movie')
        url = f"https://api.themoviedb.org/3/search/movie?query={movie_name}&include_adult=false&language=en-US&page=1"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlNTI3YWQ0MzA2N2ZkY2JiYjZjZDE2ZWE4ZjA1ZWM2MCIsIm5iZiI6MTcyNTkyNjExOS42MjY3MDYsInN1YiI6IjY0YzNjYzNiZWMzNzBjMDEzOTY3OTkxZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.15QV1PIoF0aMedTp2BtRaDiffjh_dTyBESOTruUt8eQ"
        }

        response = requests.get(url, headers=headers)

        movie_list = response.json()

        #backdrop_path = str(movie_list["results"][0]["backdrop_path"])

        #data = {
         #   "title": str(movie_list["results"][0]["original_title"]),
          #  "description":str(movie_list["results"][0]["overview"]),
           # "release": str(movie_list["results"][0]["release_date"]),
           # "backdrop_path": f"https://image.tmdb.org/t/p/w500{backdrop_path}"
        #}

        data = movie_list["results"]

        p = Paginator(data, 3)
        page = request.GET.get('page')
        movies = p.get_page(page)

    return render(request, 'movie_finder.html', {"data": data,
        "movies": movies})
# Create your views here.
