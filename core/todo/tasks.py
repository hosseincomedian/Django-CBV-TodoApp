from celery import shared_task
from .models import Todo
from core.celery import app
from celery.schedules import crontab

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=10),
        Delete_completed_tasks.s(), 
        name='completed tasks deleted'
    )


@shared_task
def Delete_completed_tasks():
    Todo.objects.filter(complete=True).delete()