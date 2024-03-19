import os

from celery import shared_task

from .predictions.predict import Predict


@shared_task
def af_predictions():
    Predict(
        "/Users/aradhya/Desktop/Uni-Projects/group-project/src/queries.csv",
        "/Users/aradhya/Desktop/Uni-Projects/group-project/src/colabparams",
    ).run()


@shared_task
def test_af_predictions() -> bool:
    import time

    time.sleep(300)
    return True


# ref: https://github.com/celery/celery/issues/6036
os.environ["FORKED_BY_MULTIPROCESSING"] = "1"
if os.name != "nt":
    from billiard import context

    context._force_start_method(
        "spawn"
    )  # 🤯 We need to spawn since our functions are not fork-safe
