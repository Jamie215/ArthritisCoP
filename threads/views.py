from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from .models import Thread, Comment
from .forms import ThreadForm, CommentForm

def thread_list(request):
    all_threads = Thread.objects.all()
    context = {
        'threads': all_threads
    }
    return render(request, 'thread_list.html', context)

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

    # Update the thread's view count
    thread.view_count += 1
    thread.save()
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

def get_sorted_threads(request):
    sort_order = request.GET.get('sort', 'recent')
    context = request.GET.get('context', 'thread_list')
    query = request.GET.get('query', '')

    if context == 'search_results' and query:
        threads = Thread.objects.filter(title__icontains=query)
    else:
        threads = Thread.objects.all()
    
    if sort_order == 'views':
        threads= threads.order_by('-view_count','-date')
    else:
        threads = Thread.objects.all().order_by('-date')

    # Check if the request is Ajax
    data = [{
            'id': thread.id,
            'title': thread.title,
            'description': thread.description,
            'date': str(thread.date),
            'view_count': thread.view_count,
            'comment_count': thread.comment_set.count()
        } for thread in threads]

    return JsonResponse(data, safe=False)