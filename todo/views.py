from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import TodoItem
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator





def register(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserRegistrationForm()

    context = {"form": form}
    return render(request, "register.html", context)


@login_required
def home(request):
    if request.method == 'POST':
        todo_name = request.POST.get("new-todo")
        todo = TodoItem.objects.create(name=todo_name, user=request.user)
        todo.save()
        return redirect("home")
    todos = TodoItem.objects.filter(is_completed=False).order_by("-id")

    paginator = Paginator(todos, 4)
    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {"todos": todos, "page_obj": page_obj}
    return render(request, "home.html", context)

def update_todo(request, pk):
    todo = get_object_or_404(TodoItem, id=pk, user=request.user)
    todo.name = request.POST.get(f"todo_{pk}")
    todo.save()
    # return redirect("home")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_todo(request, pk):
    todo = get_object_or_404(TodoItem, id=pk, user=request.user)
    todo.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def complete_todo(request, pk): 
    todo = get_object_or_404(TodoItem, id=pk, user=request.user)
    todo.is_completed = True
    todo.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Create your views here.
