from celery.result import AsyncResult  # -Line 2
from flask import jsonify, request
from tasks import flask_app, long_running_task  # -Line 1


@flask_app.get("/trigger")
def start_task() -> dict[str, object]:
    result = long_running_task.delay(int(10))  # -Line 3
    return {"result_id": result.id}


@flask_app.get("/result/<id>")
def task_result(id: str) -> dict[str, object]:
    result_id = id
    result = AsyncResult(result_id)  # -Line 4
    if result.ready():  # -Line 5
        # Task has completed
        if result.successful():  # -Line 6
            return {
                "ready": result.ready(),
                "successful": result.successful(),
                "value": result.result,  # -Line 7
            }
        else:
            # Task completed with an error
            return {"status": "ERROR", "error_message": str(result.result)}
    else:
        # Task is still pending
        return {"status": "Running"}


if __name__ == "__main__":
    flask_app.run(debug=True)
