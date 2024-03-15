from celery import shared_task

from predictions.predict import Predict

from .config import create_app

flask_app = create_app()
celery_app = flask_app.extensions["celery"]


@shared_task(ignore_result=False)
def run_predictions(
    path_to_input: str, path_to_params: str, path_to_results_dir: str
) -> None:
    Predict(
        path_to_input=path_to_input,
        path_to_params=path_to_params,
        path_to_results_dir=path_to_results_dir,
    ).run()
