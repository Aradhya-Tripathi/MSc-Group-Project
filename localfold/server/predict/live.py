import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.http.response import JsonResponse

from .models import Tasks

# Commnected out to facilitate fast predictions.
# In prod switch to af_predictions and not test_aaf_predictions.
from .tasks import af_predictions, test_af_predictions


class SignalsConsumer(JsonWebsocketConsumer):
    """Single consumer for triggering actions & receiving updates about the the action."""

    groups = ["signals"]
    model_options: dict[str, str] = (
        {}
    )  # Since they are not likely to change per perdiction
    # However they can be changed using set_model_options

    @classmethod
    def decode_json(cls, text_data):
        try:
            return json.loads(text_data)
        except json.JSONDecodeError:
            return {"error": "malformed Json"}

    def connect(self) -> None:
        """Connection handler"""
        print(f"Connecting client")
        async_to_sync(self.channel_layer.group_add)(
            "signals", self.channel_name
        )  # I can add multiple consumers to this group and then broadcast!
        self.accept()

    def disconnect(self, close_code: int) -> None:
        """Disconnect handler"""
        async_to_sync(self.channel_layer.group_discard)(
            "signals",
            self.channel_name,
        )
        # If the socket gets disconnected we will revoke all tasks since this means
        # the application is closing I don't know how I feel about this however 🤔
        # revoke_tasks(list(self.tasks.keys()))

        # Shut down the server when app is closed we don't want hanging servers
        print(f"Disconnected with close code: {close_code}")
        print("Shutting Down...")

    def receive_json(self, content, **kwargs):
        """Process appropriate method execution"""
        print(f"[RECIEVING] {content}")
        if "execute" not in content:
            self.send_json(
                {"error": "Please specify method context!"},
            )
            return
        to_execute = content["execute"]
        arg = content.get("arg")

        try:
            to_execute = getattr(self, to_execute)
        except AttributeError:
            self.send_json(
                {"error": "No such execution context!"},
            )
            return

        try:
            to_execute(arg)
        except Exception as e:
            print(e)
            self.send_json({"error": str(e)})

    def set_model_options(self, options: dict[str, str]) -> None:
        """Set model options for excution"""
        self.model_options = options

    def add_task(self, query_path: str) -> None:
        """Task addition handler"""

        if (
            "modelType" not in self.model_options
            or "modelPath" not in self.model_options
            or "resultPath" not in self.model_options
        ):
            self.send_json({"error": "Setup not complete!"})
            return

        # Figure out how to stop plot displays we don't
        # Need them in this case since it's all run by a worker
        test_af_predictions.delay(
            query_path, self.model_options
        )  # Pre-run handler takes care of sending confirmation!

    def signals_event(self, event: dict[str, str]) -> None:
        """Let the client know about the changed task"""
        self.send_json({"modifiedTask": event["taskId"]})


def get_tasks(request, taskId: str = None):
    """For now sending all the tasks will add pagination later!"""
    if taskId:
        task = Tasks.objects.get(pk=taskId)
        return JsonResponse(
            {
                "taskId": task.task_id,
                "registrationTime": task.registration_time,
                "resultDestination": task.result_destination,
                "taskStatus": task.task_status,
                "queriesPath": task.queries_path,
                "modelParameters": task.model_settings["modelPath"],
            },
            status=200,
        )

    tasks = [
        {
            "taskId": task.task_id,
            "registrationTime": task.registration_time,
            "resultDestination": task.result_destination,
            "taskStatus": task.task_status,
            "queriesPath": task.queries_path,
            "modelParameters": task.model_settings["modelPath"],
        }
        for task in Tasks.objects.all()
    ]

    return JsonResponse({"tasks": tasks}, status=200)
