from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from .models import Thread, Comment
from .forms import ThreadForm, CommentForm

def thread_list(request):
    all_threads = Thread.objects.all()
    return render(request, 'thread_list.html', {'threads': all_threads})

def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    comments = Comment.objects.filter(thread=thread).order_by('-date')

    # Handle new comment submissions
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = thread
            comment.save()
        else:
            print(form.errors)
        return redirect('thread_detail', thread_id=thread.id)
    elif request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        comments_data = [{"id": comment.id, "text": comment.text} for comment in comments]
        return JsonResponse(comments_data, safe=False)
    else:
        form = CommentForm()
        comments = Comment.objects.filter(thread=thread).order_by('-date')

    return render(request, 'thread_detail.html', {
                                                    'thread': thread, 
                                                    'comments': comments,
                                                    'form': form
                                                })

def create_thread(request):
    if request.method == "POST":
        form = ThreadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thread_list')
    else:
        form = ThreadForm()
    
    return render(request, 'create_thread.html', {'form': form})

def search_redirect(request):
    query = request.POST.get('q')
    return redirect('search_results', query=query)

def search_results(request, query):
    results = Thread.objects.filter(title__icontains=query)
    return render(request, 'search_results.html', {'results':results, 'query':query})