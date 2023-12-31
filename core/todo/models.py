from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    complete = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='photo/',blank=True)
    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-created_time",)
