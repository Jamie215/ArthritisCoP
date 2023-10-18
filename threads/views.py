from django.shortcuts import render, get_object_or_404
from .models import Thread, Comment

def thread_list(request):
    all_threads = Thread.objects.all()
    return render(request, 'thread_list.html', {'threads': all_threads})

def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    comments = Comment.objects.filter(thread=thread).order_by('-date')
    
    # Handle new comment submissions
    if request.method == "POST":
        text = request.POST.get('comment_text')
        Comment.objects.create(thread=thread, text=text)
        
    return render(request, 'thread_detail.html', {'thread': thread, 'comments': comments})

