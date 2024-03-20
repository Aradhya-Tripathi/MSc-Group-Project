import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class SignalsConsumer(JsonWebsocketConsumer):
    groups = ["singals"]

    @classmethod
    def decode_json(cls, text_data):
        try:
            return json.loads(text_data)
        except json.JSONDecodeError:
            return {"error": "malformed Json"}

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            "signals", self.channel_name
        )  # I can add multiple consumers to this group and then broadcast!
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            "signals", self.channel_name
        )  # Removing this consumer from the group on disconnect!
        print(f"Disconnected with close code: {close_code}")

    def singals_event(self, event):
        event.pop("type")
        self.send_json(content=event)

    def receive_json(self, content, **kwargs):
        self.send_json(content=content)
        return super().receive_json(content, **kwargs)
