import typing

from celery.result import AsyncResult
from core.celery import celery_handler
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .tasks import af_predictions, test_af_predictions

if typing.TYPE_CHECKING:
    from rest_framework.request import Request


@api_view(["GET"])
def is_alive(_: "Request"):
    return JsonResponse({"status": True}, status=200)


@api_view(["GET", "POST"])
def trigger(_: "Request") -> JsonResponse:
    job = test_af_predictions.delay()
    return JsonResponse({"id": job.id}, status=202)


@api_view(["GET"])
def result(_: "Request", job_id: str = None) -> JsonResponse:
    if job_id:
        result = AsyncResult(job_id)
        return JsonResponse(
            (
                {"success": result.successful(), "value": result.result}
                if result.ready()
                else {"status": result.status}
            ),
            status=200,
        )
    res = None
    active_tasks = (
        celery_handler.control.inspect().active().get("celery@AF-Predictions")
    )
    if active_tasks:
        res = active_tasks

    else:
        active_tasks = (
            celery_handler.control.inspect().reserved().get("celery@AF-Predictions")
        )

    return JsonResponse({"tasks": res}, status=200)
