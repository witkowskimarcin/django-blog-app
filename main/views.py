from django.shortcuts import render
from django.http import HttpResponse
from .models import Post, Tag
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import NewUserForm
from django.shortcuts import render, redirect

# Create your views here.

# def homepage(request):
#     return HttpResponse("Hello World!")

def homepage(request):
    return render(request = request,
                  template_name='main/home.html',
                  context = {
                      "posts":Post.objects.all,
                      "tags":Tag.objects.all})

# def show_post(request, post_title):
#     post = Post.objects.get(post_title=post_title)
#     return HttpResponse(f"{post.post_title}")

# def list_posts_by_tag(request, tag_name):
#     tag = Tag.objects.get(tag_name=tag_name)
#     return HttpResponse(f"{tag.tag_name}")

def show_post(request, post_title):
    post = Post.objects.get(post_title=post_title)
    post_tags = post.tag_set.all()
    return render(request = request,
                  template_name='main/post.html',
                  context = {
                      "post":post,
                      "post_tags":post_tags,
                      "tags":Tag.objects.all})

def list_posts_by_tag(request, tag_name):
    tag = Tag.objects.get(tag_name=tag_name)

    return render(request = request,
                  template_name='main/posts_by_tag.html',
                  context = {
                      "posts":list(tag.posts.all()),
                      "tag":tag,
                      "tags":Tag.objects.all})

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

    form = NewUserForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "main/login.html",
                    context={"form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")
