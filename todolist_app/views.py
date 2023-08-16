from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render

from todolist_app.forms import TaskForm

from .models import TaskList


@login_required
def todolist(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.owner = request.user  # adding the user details to the task
            inst.save()

        messages.success(request, "Task Added Successfully")
        return redirect("todolist")
    else:
        all_tasks = TaskList.objects.filter(owner=request.user)
        paginator = Paginator(all_tasks, 5)
        page = request.GET.get("pg")
        all_tasks = paginator.get_page(page)
        # return HttpResponse('Welcome to Task Page')
        # return render(request, 'todolist.html', {'welcome_text': 'Welcome to Task Page'})
        return render(request, "todolist.html", {"all_tasks": all_tasks})


@login_required
def delete_task(
    request, task_id
):  # var name 'task_id' shd match name used in path in urls.py
    task = TaskList.objects.get(pk=task_id)
    if task.owner == request.user:
        task.delete()
    else:
        messages.error(
            request, ("Access Restricted; you are NOT the owner of this task")
        )
    return redirect("todolist")


@login_required
def complete_task(
    request, task_id
):  # var name 'task_id' shd match name used in path in urls.py
    task = TaskList.objects.get(pk=task_id)
    if task.owner == request.user:
        task.done = True
        task.save()
    else:
        messages.error(
            request, ("Access Restricted; you are NOT the owner of this task")
        )

    return redirect("todolist")


@login_required
def mark_pending(
    request, task_id
):  # var name 'task_id' shd match name used in path in urls.py
    task = TaskList.objects.get(pk=task_id)
    if task.owner == request.user:
        task.done = False
        task.save()
    else:
        messages.error(
            request, ("Access Restricted; you are NOT the owner of this task")
        )

    return redirect("todolist")


@login_required
def edit_task(request, task_id):  # var name 'task_id' shd match name used
    if request.method == "POST":
        task_obj = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST or None, instance=task_obj)
        if form.is_valid():
            form.save()
        messages.success(request, "Task Edited Successfully")
        return redirect("todolist")
    else:
        task_obj = TaskList.objects.get(pk=task_id)
        return render(request, "edit.html", {"task_obj": task_obj})


def index(request):
    return render(request, "index.html", {"index_text": "Welcome to Home Page"})


def about(request):
    return render(request, "about.html", {"about_text": "Welcome to About Page"})


def contact(request):
    return render(request, "contact.html", {"contact_text": "Welcome to Contact Page"})
