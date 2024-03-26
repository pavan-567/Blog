from django.shortcuts import get_object_or_404, redirect, render
from .models import Post
from Auth.models import User 
from Category.models import Category
from Replies.models import Reply
from .forms import PostForm
from Comments.forms import CommentForm
from Category.forms import CategoryForm
from Comments.models import Comment
from django.core import serializers
from django.core.paginator import Paginator

# Create your views here.
def Home(request) : 
    # Searching Via Query Parameter
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    # Getting Posts Based On Search Results
    posts = Post.objects.filter(category__name__icontains= q)

    # Specific Post Count
    posts_count = posts.count()

    # All Posts Count
    total_posts = Post.objects.all().count()

    # Getting Users
    users = User.objects.all()
    top_users = []

    # Getting Users With Count Of Their Posts .. The Sorting Is Done Inside The Template
    for user in users if len(users) > 0 else "" : 
        top_post = Post.objects.filter(author= user)
        if top_post.count() > 0 : 
            top_users.append({'user': user, 'count': top_post.count()})


    # print(f"Top Users : {top_users}")
            
    # Creating Pagination
    p = Paginator(posts, 2)
    page = request.GET.get('page')
    posts_per_page = p.get_page(page)

    context = {
        "posts": posts_per_page,
        "categories": Category.objects.all(),
        "count": posts_count,
        "top_users": top_users[:5],
        "total_posts": total_posts,
        "current_category": q,
        "form": PostForm(),
        "c_form": CategoryForm(),
        "page_loops": "a" * posts_per_page.paginator.num_pages
    }

    return render(request, "Posts/Home.html", context)



def Create(request) : 
    form = PostForm() 

    if request.method == "POST" : 
        form = PostForm(request.POST, request.FILES)
        if form.is_valid() : 
            post = form.save(commit= False)
            post.author = request.user 
            post.save()

            return redirect('home')
    
    context = {
        "form": form 
    }

    return render(request, "Posts/create.html", context)


def Edit(request, pk) : 
    if not request.user.is_authenticated : 
        return redirect('home')
    
    current_post = Post.objects.get(id= pk)

    if not request.user.id == current_post.author.id : 
        return redirect('home')
    
    form = PostForm(instance= current_post)

    if request.method == "POST" : 
        form = PostForm(request.POST, request.FILES, instance= current_post)
        if form.is_valid() : 
            form.save() 
            return redirect('detail-post', pk= pk)
        
    context = {'form': form, 'post' : current_post}
    return render(request, "Posts/edit.html", context)


def Delete(request, pk) : 
    if not request.user.is_authenticated : 
        return redirect('home')
    
    current_post = Post.objects.get(id= pk)

    if not request.user.id == current_post.author.id : 
        return redirect('home')
    
    if request.method == "POST" : 
        current_post.delete()
        return redirect('home')
    
    return render(request, "Posts/delete.html", {'post': current_post})


def Detail(request, pk) : 
    current_post = Post.objects.get(id= pk)
    comments = Comment.objects.filter(post= current_post)

    liked = False 

    if current_post.likes.filter(id= request.user.id).exists() : 
        liked = True

    comments_count = comments.count()
    comments_serializer = serializers.serialize('json', comments, ensure_ascii= False)

    form = CommentForm()
    
    context = {
        "post": current_post,
        "comments": comments,
        "comments_js": comments_serializer,
        "form": form, 
        "count": comments_count,
        "liked": liked,
        "editForm": PostForm(instance= current_post),
        "replies": Reply.objects.all()
    }

    return render(request, "Posts/detail.html", context)


def LikePost(request, pk) : 
    print(request.POST)
    post = get_object_or_404(Post, id= request.POST.get('post_id'))

    if post.likes.filter(id= request.user.id).exists() : 
        post.likes.remove(request.user)
    else : 
        post.likes.add(request.user)
    return redirect('detail-post', pk= pk)

