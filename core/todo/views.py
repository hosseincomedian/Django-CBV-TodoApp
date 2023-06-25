from django.views.generic import ListView, CreateView, DeleteView, UpdateView, View
from .models import Todo
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


class TodoListView(LoginRequiredMixin, ListView):
    model = Todo

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    fields = ["title", "complete"]
    success_url = reverse_lazy("todo-list")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


class TodoCompleteView(LoginRequiredMixin, View):
    """
    use by JS
    """

    def post(self, request, *args, **kwargs):
        todo = Todo.objects.get(pk=request.POST.get("todo_id"))
        todo.complete = not todo.complete
        todo.save()
        return HttpResponse("ok")


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = ["title", "complete"]
    success_url = reverse_lazy("todo-list")

    def get_object(self, *args, **kwargs):
        print("ok")
        todo = get_object_or_404(Todo, pk=self.kwargs.get("pk"), user=self.request.user)
        return todo


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    success_url = reverse_lazy("todo-list")

    def get_object(self, *args, **kwargs):
        todo = get_object_or_404(Todo, pk=self.kwargs.get("pk"), user=self.request.user)
        return todo
