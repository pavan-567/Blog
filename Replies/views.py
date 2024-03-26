from django.shortcuts import render
from .models import Reply
from Comments.models import Comment
from django.shortcuts import get_object_or_404, redirect, render


# Create your views here.
def LikeReply(request, pk) : 
    reply = get_object_or_404(Reply, id= request.POST.get('reply_id'))

    if reply.likes.filter(id= request.user.id).exists() : 
        reply.likes.remove(request.user)
    else : 
        reply.likes.add(request.user)
    return redirect('detail-post', pk= pk)

def Create(request, comment_id) : 
    comment = Comment.objects.get(id= comment_id)

    if request.method == "POST" : 
        reply = request.POST.get('reply')
        Reply.objects.create(comment= comment, user= request.user, reply= reply)

    return redirect('detail-post', pk= comment.post.id)

def Edit(request, pk) :
    # Pk : Replies Primary Key
    if not request.user.is_authenticated : 
        return redirect('home')
    
    reply = Reply.objects.get(id= pk)

    comment_reply_id = reply.comment.id 
    comment_post_id = reply.comment.post.id 

    if not request.user.id == reply.user.id : 
        return redirect('home')
    
    if request.method == "POST" : 
        reply_text = request.POST.get('reply')
        reply.reply = reply_text
        reply.save()
        return redirect('detail-post', pk= comment_post_id)
    
def Delete(request, pk) : 
    # Pk : Replies Primary Key
    if not request.user.is_authenticated : 
        return redirect('home')
    
    reply = Reply.objects.get(id= pk)
    comment_reply_id = reply.comment.id 
    comment_post_id = reply.comment.post.id 

    if not request.user.id == reply.user.id  : 
        return redirect('home')
    
    if request.method == "POST" :
        reply.delete()
        return redirect('detail-post', pk= comment_post_id)
    