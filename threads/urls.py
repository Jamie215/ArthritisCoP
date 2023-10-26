from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.thread_list, name='thread_list'),
    path('get_sorted_threads/', views.get_sorted_threads, name='get_sorted_threads'),
    path('<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('create/', views.create_thread, name='create_thread'),
    path('search/', views.search_redirect, name='search_redirect'),
    path('search/<str:query>/', views.search_results, name='search_results'),
    path('delete_thread/<int:thread_id>/', views.delete_thread, name='delete_thread')
]