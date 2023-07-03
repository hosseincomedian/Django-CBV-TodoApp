from celery import shared_task
from todo.models import Todo

@shared_task
def Delete_completed_tasks():
    Todo.objects.filter(complete=True).delete()