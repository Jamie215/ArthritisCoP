from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Thread, Comment
from .forms import ThreadForm, CommentForm, SignUpForm
from django.contrib.auth.forms import AuthenticationForm

##################
## User Related ##
##################

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data/get('password2')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form':form})

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form':form})

###############################
## Thread & Comment Related ##
##############################

def thread_list(request):
    all_threads = Thread.objects.all()
    
    # Check if the user is a moderator
    is_moderator= request.user.groups.filter(name='Moderators').exists() or request.user.is_superuser

    context = {
        'results': all_threads,
        'is_moderator': is_moderator
    }

    return render(request, 'thread_list.html', context)

def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    comments = Comment.objects.filter(thread=thread).order_by('-date')

    # Check if the user is a moderator
    is_moderator= request.user.groups.filter(name='Moderators').exists() or request.user.is_superuser

    # Handle new comment submissions
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.thread = thread
            comment.save()
        else:
            print(form.errors)
        return redirect('thread_detail', thread_id=thread.id)
    elif request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        comments_data = [{"id": comment.id, 
                          "text": comment.text,
                          "date": comment.date.strftime('%Y-%m-%d %H:%M:%S'),
                          "upvotes": comment.upvotes,
                          "downvotes": comment.downvotes}
                          for comment in comments]
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
                                                    'form': form,
                                                    'is_moderator': is_moderator
                                                })

def create_thread(request):
    if request.method == "POST":
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            return redirect('thread_list')
    else:
        form = ThreadForm()
    
    return render(request, 'create_thread.html', {'form': form})

def search_redirect(request):
    query = request.POST.get('q')
    return redirect('search_results', query=query)

def search_results(request, query):
    results = Thread.objects.filter(title__icontains=query)
    is_moderator= request.user.groups.filter(name='Moderators').exists() or request.user.is_superuser

    context = {
        'results': results,
        'is_moderator': is_moderator,
        'query': query,
    }

    return render(request, 'search_results.html', context)

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

@login_required
@require_http_methods(["DELETE"])
def delete_thread(request, thread_id):
    try:
        if not (request.user.groups.filter(name='Moderators').exists() or request.user.is_superuser):
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        
        thread = get_object_or_404(Thread, id=thread_id)
        thread.delete()
        return JsonResponse({'message': 'Thread successfully deleted'})
    
    except Thread.DoesNotExist:
        return JsonResponse({'message': 'Thread does not exist'}, status=404)
    
    except Exception as e:
        return JsonResponse({'message': e}, status=500)

@login_required
@require_http_methods(["DELETE"])
def delete_comment(request, comment_id):
    try:
        if not (request.user.groups.filter(name='Moderators').exists() or request.user.is_superuser):
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
        return JsonResponse({'message': 'Comment successfully deleted'})
    
    except Comment.DoesNotExist:
        return JsonResponse({'message': 'Comment does not exist'}, status=404)
    
    except Exception as e:
        return JsonResponse({'message': e}, status=500)
