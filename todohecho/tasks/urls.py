from django.urls import path
from . import views


####

app_name = 'tasks'

urlpatterns = [
    path('create_task/',views.TaskCreate.as_view(),name="create"),
    path("<int:pk>", views.TaskDetailView.as_view(),name="task_detail"),
    path("tasks/",views.TaskListView.as_view(),name="tasks"),
    path("tasks/complete",views.CompleteListView.as_view(),name="tasks_complete"),
    path("tasks/<int:pk>/edit",views.TaskModify.as_view(),name="edit"),
    path("task/<int:pk>/delete",views.TaskDelete.as_view(),name="delete"),
    path("task/<int:pk>/uncomplete",views.uncomplete_task, name="uncomplete"),
    path("task/<int:pk>/complete",views.complete_task, name="complete"),

]
