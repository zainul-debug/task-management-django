
import json
from datetime import date

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


@csrf_exempt
@require_POST
def check_overdue_tasks(request):
    """
    Receive tasks from Laravel and identify tasks
    that are overdue and not already DONE.
    """
    try:
        data = json.loads(request.body)
        tasks = data.get("tasks", [])
        today = date.today()
        overdue_tasks = []

        for task in tasks:
            due_date = date.fromisoformat(task["due_date"])
            status = task["status"]

            if due_date < today and status != "DONE":
                overdue_tasks.append({
                    "id": task["id"],
                    "status": "OVERDUE",
                })

        return JsonResponse({
            "success": True,
            "checked_on": today.isoformat(),
            "overdue_tasks": overdue_tasks,
        })

    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        return JsonResponse({
            "success": False,
            "message": "Invalid task data. Check the task IDs, due dates, and statuses.",
        }, status=400)
