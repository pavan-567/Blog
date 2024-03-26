from django.shortcuts import get_object_or_404, redirect, render
from .forms import CommentForm
from .models import Comment
from Posts.models import Post

# Create your views here.

def Create(request, post_id) :
    post = Post.objects.get(id= post_id)

    form = CommentForm()

    if request.method == "POST": 
        form = CommentForm(request.POST)
        if form.is_valid() : 
            comment = form.save(commit= False)
            comment.user = request.user 
            comment.post = post
            comment.save()

    return redirect('detail-post', pk= post_id)


def Edit(request, pk) : 
    if not request.user.is_authenticated : 
        return redirect('home')
    
    comment = Comment.objects.get(id= pk)

    comment_post_id = comment.post.id 

    if not request.user.id == comment.user.id : 
        return redirect('home')
    
    form = CommentForm(instance= comment)


    if request.method == "POST" : 
        form = CommentForm(request.POST, instance= comment)
        print(f"Valid : {form.is_valid()}")
        if form.is_valid() : 
            form.save()
            return redirect('detail-post', pk= comment_post_id)
    
    context = {
        'form': form,
        'post_belong': comment_post_id,
        'a' : 10
    }

    return render(request, 'Comments/edit.html', context)


def Delete(request, pk) : 
    if not request.user.is_authenticated: 
        return redirect('home')
    
    comment = Comment.objects.get(id= pk)

    post_of_comment = comment.post.id 

    if not request.user.id == comment.user.id : 
        return redirect('home')

    if request.method == "POST" : 
        comment.delete() 

        return redirect('detail-post', pk= post_of_comment)

    context = {'comment': comment}
    return render(request, 'Comments/delete.html', context)

 
def LikeComment(request, pk) : 
    comment = get_object_or_404(Comment, id= request.POST.get('comment_id'))

    if comment.likes.filter(id= request.user.id).exists() : 
        comment.likes.remove(request.user)
    else : 
        comment.likes.add(request.user)
    return redirect('detail-post', pk= pk)