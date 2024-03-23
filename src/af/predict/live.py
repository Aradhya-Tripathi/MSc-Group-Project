import json
import os
import signal
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from .tasks import af_predictions, revoke_tasks, test_af_predictions


class SignalsConsumer(JsonWebsocketConsumer):
    groups = ["signals"]
    tasks: dict[str, str] = {}
    colabparams: str = None

    @classmethod
    def decode_json(cls, text_data):
        try:
            return json.loads(text_data)
        except json.JSONDecodeError:
            return {"error": "malformed Json"}

    def connect(self) -> None:
        """Connection handler"""
        async_to_sync(self.channel_layer.group_add)(
            "signals", self.channel_name
        )  # I can add multiple consumers to this group and then broadcast!
        self.accept()

    def disconnect(self, close_code: int) -> None:
        """Disconnect handler"""
        async_to_sync(self.channel_layer.group_discard)(
            "signals", self.channel_name
        )  # Removing this consumer from the group on disconnect!
        # If the socket gets disconnected we will revoke all tasks since this means
        # the application is closing I don't know how I feel about this however 🤔
        revoke_tasks(list(self.tasks.keys()))
        self.tasks = {}

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
        # Fetch the method
        try:
            to_execute = getattr(self, to_execute)
        except AttributeError:
            self.send_json(
                {"error": "No such execution context!"},
            )
            return
        # Execute the method
        try:
            to_execute(arg)
        except Exception as e:
            print(e)
            self.send_json({"error": str(e)})

    def set_model_path(self, path: str) -> None:
        self.colabparams = path

    def add_task(self, query_path: str) -> None:
        """Task addition handler"""
        if len(self.tasks) > 10:  # Not showing more than 10 tasks
            self.tasks = (
                {}
            )  # Figure this out there should be a better way of handling this!

        if not self.colabparams:
            self.send_json({"error": "Setup not complete!"})
            return

        job = test_af_predictions.delay(
            query_path, self.colabparams
        )  # Pre-run handler takes care of sending confirmation!
        self.tasks[job.id] = "unknown"

    def signals_event(self, event: dict[str, str]) -> None:
        """Events handler"""
        self.tasks[event["taskId"]] = event[
            "status"
        ]  # update task status when event is recieved
        self.send_json(content={"tasks": self.tasks})
