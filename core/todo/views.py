from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, View
from .models import Todo
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponse

class TodoListView(LoginRequiredMixin, ListView):
    model = Todo

    def get_queryset(self):
        return self.model.objects.filter(user = self.request.user)


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    fields = ["title", 'complete']
    success_url = reverse_lazy('todo-list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()        
        return super().form_valid(form)

class TodoCompleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        todo = Todo.objects.get(pk=request.POST.get('todo_id'))
        todo.complete = not todo.complete
        todo.save()
        return HttpResponse("ok")

class TodoUpdateView(UpdateView):
    pass

class TodoDeleteView(DeleteView):
    pass