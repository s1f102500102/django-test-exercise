from django.shortcuts import render, redirect
from django.http import Http404
from django.utils import timezone
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from todo.models import Task


def index(request):
    if request.method == 'POST':
        task = Task(
            title=request.POST['title'],
            due_at=make_aware(parse_datetime(request.POST['due_at']))
        )
        task.save()

    order = request.GET.get("order")

    if order == "due":
        tasks = Task.objects.order_by("due_at")
    elif order == "post":
        tasks = Task.objects.order_by("-id")
    else:
        tasks = Task.objects.order_by("id")

    total_count = tasks.count()
    completed_count = tasks.filter(completed=True).count()
    overdue_count = tasks.filter(completed=False, due_at__lt=timezone.now()).count()
    completion_rate = round(completed_count / total_count * 100) if total_count else 0

    context = {
        'tasks': tasks,
        'total_count': total_count,
        'completed_count': completed_count,
        'overdue_count': overdue_count,
        'completion_rate': completion_rate,
    }
    return render(request, 'todo/index.html', context)


def detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    
    context = {
        "task": task,
    }
    return render(request, "todo/detail.html", context)

def update(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404('Task does not exist')
    if request.method == 'POST':
        task.title = request.POST['title']
        task.due_at = make_aware(parse_datetime(request.POST['due_at']))
        task.save()
        return redirect(detail, task_id)

    context = {
        'task': task
    }
    return render(request, "todo/edit.html", context)

def delete(request,task_id):
    try:
        task=Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404('Task does not exist')
    task.delete()
    return redirect(index)

def toggle(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404('Task does not exist')
    task.completed = not task.completed
    task.save()
    return redirect(detail, task_id)

