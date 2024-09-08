from .models import Post
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm

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

# Create your views here.
