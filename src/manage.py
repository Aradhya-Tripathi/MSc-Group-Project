from celery.result import AsyncResult
from server.tasks import flask_app, run_predictions


@flask_app.get("/trigger")
def start_task() -> dict[str, object]:
    result = run_predictions.delay(
        path_to_input="./queries.csv",
        path_to_params="./colabparams",
        path_to_results_dir="./results",
    )
    return {"result_id": result.id}


@flask_app.get("/result/<id>")
def task_result(id: str) -> dict[str, object]:
    result_id = id
    result = AsyncResult(result_id)
    return (
        {"success": result.successful(), "value": result.value()}
        if result.ready()
        else {"status": "Running"}
    )


if __name__ == "__main__":
    flask_app.run(debug=True)
