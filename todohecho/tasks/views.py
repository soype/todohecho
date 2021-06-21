from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views import generic
from .models import Task

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from accounts import models as accounts

# Create your views here.

# Post Detail, Post List, PostCreat, PostDelete, PostModify

class TaskCreate(generic.CreateView,LoginRequiredMixin):
    login_url = '/accounts/login/'
    model = Task
    fields = ("title","description", "priority_number")
    # redirect_field_name = "tasks/task_detail.html"
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

class TaskDetailView(generic.DetailView,LoginRequiredMixin):
    model = Task
    context_object_name = "task"
    # template_name = "tasks/task_detail.html"

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
           context = super().get_context_data(**kwargs)
            
           return context
        else:
            return Task.objects.none()

        
class TaskListView(generic.ListView, LoginRequiredMixin):
    #No funciona
    login_url = 'accounts:login'
    model = Task, accounts.Account
    paginate_by = 10
    fields = ("title","author")
    context_object_name = 'tasks'
    template_name="tasks/task_list.html"
    
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Task.objects.filter(author = self.request.user, completed_date__isnull=True).order_by("priority_number")
        else:
            return Task.objects.none()
        

class CompleteListView(generic.ListView):
    #No funciona
    model = Task, accounts.Account
    login_url = '/accounts/login/'
    paginate_by = 10
    fields = ("title","author")
    context_object_name = 'tasks'
    template_name="tasks/complete_list.html"
    
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Task.objects.filter(author = self.request.user, completed_date__isnull=False).order_by("priority_number")
        else:
            return Task.objects.none()


    
class TaskModify(generic.UpdateView,LoginRequiredMixin):
    model = Task
    redirect_field_name="tasks/taks_detail.html"
    fields = ("title","description","priority_number")
    

class TaskDelete(generic.DeleteView,LoginRequiredMixin):
    model = Task
    success_url = reverse_lazy('tasks:tasks')
    

    
def uncomplete_task(request,pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Task,pk=pk)
        post.uncomplete()
        return redirect('tasks:task_detail',pk=pk)

def complete_task(request,pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Task,pk=pk)
        post.complete()
        return redirect('tasks:tasks')