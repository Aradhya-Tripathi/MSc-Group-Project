import typing

from celery.result import AsyncResult
from django.http.response import JsonResponse
from rest_framework.decorators import api_view

from .tasks import af_predictions

if typing.TYPE_CHECKING:
    ...


@api_view(["GET", "POST"])
def trigger(request):
    job = af_predictions.delay()
    return JsonResponse({"id": job.id}, status=202)


@api_view(["GET"])
def result(request, id: str):
    result_id = id
    result = AsyncResult(result_id)
    return JsonResponse(
        {"success": result.successful(), "value": result.result}
        if result.ready()
        else {"status": "Running"}
    )
