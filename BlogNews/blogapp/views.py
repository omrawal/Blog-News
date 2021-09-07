from .forms import PostCreate
from django.shortcuts import render, redirect
from .models import Post
# Create your views here.
from django.http import HttpResponse
import requests
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


@login_required(login_url='login')
def index(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'index.html', context)
    return render(request, 'index.html')


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {'form': AuthenticationForm()}
        return render(request, 'login.html', context)
    return render(request, 'login.html')


def logoutPage(request):
    logout(request)
    return render(request, 'logout.html')


def registerPage(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'register.html', context)


@login_required(login_url='login')
def news(request):
    # key ='dfdf852152b9441e8f197844bc6f9226'
    api_link = 'https://newsapi.org/v2/top-headlines?country=in&apiKey=dfdf852152b9441e8f197844bc6f9226'
    api_get = requests.get(api_link)
    api_get_json = api_get.json()
    news_dict = {}
    for i, article in enumerate(api_get_json['articles']):
        temp_dict = {'img_url': article['urlToImage'], 'author': article['source']['name'], 'title': article['title'], 'description': article['description'],
                     'url': article['url'], }
        news_dict[i] = temp_dict

    return render(request, 'news.html', {'context': news_dict})


@login_required(login_url='login')
def upload(request):
    upload = PostCreate()
    if request.method == 'POST':
        upload = PostCreate(request.POST, request.FILES)
        if upload.is_valid():
            upload.save()
            return redirect('index')
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    else:
        return render(request, 'upload_form.html', {'upload_form': upload})


@login_required(login_url='login')
def update_post(request, post_id):
    item = Post.objects.get(id=post_id)
    if(request.user == item.author or request.user.is_staff):
        post_id = int(post_id)
        try:
            post_rem = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return redirect('index')
        post_form = PostCreate(request.POST or None, instance=post_rem)
        if post_form.is_valid():
            post_form.save()
            return redirect('index')
    return render(request, 'upload_form.html', {'upload_form': post_form})


@login_required(login_url='login')
def delete_post(request, post_id):
    item = Post.objects.get(id=post_id)
    if(request.user == item.author or request.user.is_staff):
        post_id = int(post_id)
        try:
            post_sel = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return redirect('index')
        post_sel.delete()
    return redirect('index')
