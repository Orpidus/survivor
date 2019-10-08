from django.urls import path

from task.views import TaskView

urlpatterns = [
    path('<int:survivor_id>/', TaskView.as_view(), name='task'),
]
