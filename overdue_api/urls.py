
from django.urls import path
from .views import check_overdue_tasks

urlpatterns = [
    path("check-overdue/", check_overdue_tasks, name="check_overdue_tasks"),
]
