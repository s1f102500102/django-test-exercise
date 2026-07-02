from django.shortcuts import render, redirect
from django.http import Http404
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

    context = {
        'tasks': tasks
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
        return redirect(detail, task_id)

    context = {
        'task': task
    }
    return render(request, "todo/edit.html", context)