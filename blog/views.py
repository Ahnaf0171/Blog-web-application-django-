from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from blog import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import Post_form, comment_form
from django.contrib import messages
from django.db.models import Q
# Create your views here.

def post_list(request):
    categoryQ = request.GET.get('category', None)
    tagQ = request.GET.get('tag', None)
    search_query = request.GET.get('q', None)
    if categoryQ:
        posts = models.Post.objects.filter(category_id__name = categoryQ)
    elif tagQ:
        posts = models.Post.objects.filter(tag__name = tagQ)
    else:
        posts = models.Post.objects.all()

    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(tag__name__icontains=search_query) |
            Q(category_id__name__icontains=search_query)
        ).distinct()

    category = models.Category.objects.all()
    tag = models.Tag.objects.all()

    return render(request, 'blog/post_list.html',{'posts':posts, 'categories':category, 'tags': tag} )

def post_details(request, id):
    post = get_object_or_404(models.Post, id=id)
    category = models.Category.objects.all()
    tag = models.Tag.objects.all()
    
    #comments = Comments.objects.filter(post=post)
    if request.method=="POST":
        commentform = comment_form(request.POST)
        if commentform.is_valid():
            comment = commentform.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            commentform = comment_form()

    else:
        commentform = comment_form()
    
    #comments = Comments.objects.filter(post=post)
    comments = post.comment_set.all()
    is_liked = False
    if post.liked_users.filter(id=request.user.id):
        is_liked= True
    else:
        is_liked = False
    
    post.view_count +=1 
    post.save()
    like_count = post.liked_users.count()

    context = {'post': post, 'categories':category, 'tags':tag, 
               'comments':comments, 'comment_form':commentform, 'is_liked': is_liked, 'like_count':like_count} 

    return render(request, 'blog/post_details.html',context)

@login_required
def like_post(request, id):
    post = get_object_or_404(models.Post, id=id)
    if post.liked_users.filter(id=request.user.id):
        post.liked_users.remove(request.user)
    else:
        post.liked_users.add(request.user)
    return redirect("post_details", id=post.id)


def user_sign_up(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    context = {"form":form}
    return render(request,'blog/registration/login.html', context)

@login_required
def create_post(request):
    if request.method == "POST":
        form = models.Post(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
        
    else:        
        form = models.Post()
    return render(request, 'blog/create_post.html', {"form":form})

def create_post(request):
    if request.method =="POST":
        form = Post_form(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')

    else:
        form = Post_form()
    return render(request, 'blog/create_post.html',{"form":form})

def update_post(request, id):
    post = get_object_or_404(models.Post, id=id)

    if request.user != post.author:
        messages.error(request, "You cannot change this post")
        return redirect('post_details', id= post.id)
    if request.method=="POST":
        form = Post_form(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "post updated successfully")
            return redirect('post_list')
    else: 
        form = Post_form(instance=post)
    return render(request,'blog/create_post.html',{"form":form})

def delete_post(request, id):
    post = get_object_or_404(models.Post, id=id)
    if request.user != post.author:
        messages.error(request,"You cannot delete this post")
        return redirect('post_list', id = post.id)
    else:
        post.delete()
        messages.success(request, "Post Deleted successfully")
    return redirect('post_list')





