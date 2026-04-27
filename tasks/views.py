from typing import Any

from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Task
from .forms import CreateTaskForm, TaskEditForm

def index(request):
    return render(request, "tasks/index.html")

@login_required(login_url="/accounts/login/")
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by("-due_at")
    
    return render(
        request, 
        "tasks/task_list.html", 
        context={ 
            'todo_tasks': tasks.filter(status='todo'),
            'doing_tasks': tasks.filter(status='doing'),  
            'done_tasks': tasks.filter(status='done'),      
            'todo_count': tasks.filter(status='todo').count(),
            'doing_count': tasks.filter(status='doing').count(),
            'done_count': tasks.filter(status='done').count(),
        }
    ) 

@login_required(login_url="/accounts/login/")
@require_POST
def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    new_status = request.POST.get('status')
    new_title = request.POST.get('title')
    new_desc = request.POST.get('desc')
    
    if new_status in dict(Task.Status.choices):
        task.status = new_status
        task.save(update_fields=['status'])
        
    # Se vier de fetch (drag & drop), retorna JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'ok': True, 'status': task.status})

    # Se vier de form normal (botões), redireciona
    return redirect(request.META.get('HTTP_REFERER', 'tasks:list'))

@login_required(login_url="/accounts/login/")
def task_create(request):
    if request.method == "POST":
        form = CreateTaskForm(request.POST)
        
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            
            return redirect('tasks:list')

    form = CreateTaskForm()
    
    return render(
        request,
        "tasks/tasks_form.html",
        {
            "form": form
        }
    )

@login_required(login_url="/accounts/login/")
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    return render(request, 'tasks/task_detail.html', {
        'task': task
    })
    
@login_required(login_url="/accounts/login/")
@require_POST
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    return redirect('tasks:list')

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskEditForm
    template_name = 'tasks/task_edit.html'
    login_url = '/accounts/login/'
    
    def get_queryset(self) -> QuerySet[Any]:
        return Task.objects.filter(user=self.request.user)
    
    def get_success_url(self) -> str:
        return reverse_lazy('tasks:detail', kwargs={'pk': self.get_object().pk})

