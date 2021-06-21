from django.db import models
from accounts.models import Account
from django.urls import reverse
from django.utils import timezone

# Create your models here.

class Priority(models.Model):
    priority = models.IntegerField()

    def __str__(self):
        return str(self.priority)

class Task(models.Model):
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=180)
    author = models.ForeignKey(Account, related_name='author', null=True, blank=True, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now=True)
    completed_date = models.DateField(blank=True, null=True)
    priority_number = models.ForeignKey(Priority, related_name="priority_number", null=True, blank=True, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tasks:task_detail', kwargs={'pk':self.pk})
        # return reverse("home", kwargs={"pk": self.pk}) 

    def complete(self):
        self.completed_date = timezone.now()
        self.save()

    def uncomplete(self):
        self.completed_date = None
        self.save()
