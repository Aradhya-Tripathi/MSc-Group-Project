import os

from celery import shared_task
from celery.signals import task_prerun, task_success
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .predictions.predict import Predict


def revoke_tasks(task_ids: list[str]) -> None:
    from core.celery import celery_handler

    # Revoke and terminate the worker child process executing the task
    celery_handler.control.revoke(task_ids, terminate=True)


@task_prerun.connect
def task_prerun_handler(sender=None, **kargs) -> None:
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "signals",
        {
            "type": "signals.event",
            "taskId": f"{sender.request.id}",
            "status": "running",
        },
    )


@task_success.connect
def task_success_handler(sender=None, **kwargs) -> None:
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "signals",
        {
            "type": "signals.event",
            "taskId": f"{sender.request.id}",
            "status": "successful",
        },
    )


@shared_task
def af_predictions(query_path, colabparams):
    Predict(query_path, colabparams).run()


@shared_task
def test_af_predictions(query_path, colabparams) -> bool:
    import time

    print(query_path, colabparams)

    time.sleep(30)
    return True


# ref: https://github.com/celery/celery/issues/6036
os.environ["FORKED_BY_MULTIPROCESSING"] = "1"
if os.name != "nt":
    from billiard import context

    context._force_start_method(
        "spawn"
    )  # 🤯 We need to spawn since our functions are not fork-safe
