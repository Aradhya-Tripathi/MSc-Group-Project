import os

from celery import shared_task

from .predictions.predict import Predict


@shared_task
def af_predictions():
    Predict(
        "/Users/aradhya/Desktop/Uni-Projects/group-project/src/queries.csv",
        "/Users/aradhya/Desktop/Uni-Projects/group-project/src/colabparams",
    ).run()


# ref: https://github.com/celery/celery/issues/6036
os.environ["FORKED_BY_MULTIPROCESSING"] = "1"
if os.name != "nt":
    from billiard import context

    context._force_start_method(
        "spawn"
    )  # 🤯 We need to spawn since our functions are not fork-safe
