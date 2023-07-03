# from core.celery import app
# from todo.tasks import Delete_completed_tasks

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(
#         10,
#         Delete_completed_tasks.s(), 
#         name='completed tasks deleted'
#     )