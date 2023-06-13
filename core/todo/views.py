from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView
from .models import Todo
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class TodoListView(LoginRequiredMixin, ListView):
    model = Todo


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    fields = ["title", 'complete']
    success_url = reverse_lazy('todo-list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()        
        return super().form_valid(form)