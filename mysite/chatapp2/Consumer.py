from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from .models import usersidle


class Consumer(WebsocketConsumer):
    def connect(self):
        self.person_name = self.scope["url_route"]["kwargs"]["person_name"]
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat",
                "message": "waiting for stranger",
                "person": self.person_name,
                "action": "join",
                "channelname": self.channel_name,
                "group": self.room_group_name,
            },
        )
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat",
                "message": " has disconnected",
                "person": self.person_name,
                "action": "disconnected",
                "channelname": self.channel_name,
                "group": self.room_group_name,
            },
        )
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        if usersidle.objects.filter(
            name=self.person_name, roomid=self.room_name
        ).exists():
            u = usersidle.objects.get(name=self.person_name, roomid=self.room_name)
            u.delete()

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat",
                "message": message,
                "person": self.person_name,
                "action": "messaging",
                "channelname": self.channel_name,
                "group": self.room_group_name,
            },
        )

    def chat(self, event):
        group = event["group"]
        action = event["action"]
        person = event["person"]
        message = event["message"]
        channel = event["channelname"]
        self.send(
            text_data=json.dumps(
                {
                    "group": group,
                    "message": message,
                    "person": person,
                    "action": action,
                    "channel": channel,
                }
            )
        )
