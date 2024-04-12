import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Contact, Message
from user.models import User
from group.models import Group
from .controllers import get_user_status, get_user_contacts, is_group


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.username = self.scope["url_route"]["kwargs"]["channel_name"]
        async_to_sync(self.channel_layer.group_add)(
            self.username,
            self.channel_name,
        )
        self.accept()

        status = get_user_status(self.username)
        if status == "offline":
            user_contacts = get_user_contacts(self.username)
            for contact in user_contacts:
                self.send_data_to_user(
                    contact["username"],
                    "update_status",
                    {"target": self.username, "status": "online"},
                )
        user = User.objects.get(username=self.username)
        user.increment_socket()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.username,
            self.channel_name,
        )
        user = User.objects.get(username=self.username)
        user.decrement_socket()
        status = get_user_status(self.username)
        if status == "offline":
            user_contacts = get_user_contacts(self.username)
            for contact in user_contacts:
                self.send_data_to_user(
                    contact["username"],
                    "update_status",
                    {"target": self.username, "status": "offline"},
                )

    def receive(self, text_data):
        data = json.loads(text_data)
        type = data["type"]
        if type == "SEND_MESSAGE":
            self.handleSendMessage(data)
        self.send(
            text_data=json.dumps(
                {
                    "message": "OK",
                }
            )
        )

    def handleSendMessage(self, event):
        data = event["message"]
        data["sender"] = self.username
        receiver = data["receiver"]
        sender = data["sender"]
        message = data["message"]
        receiver_type = "group" if is_group(receiver) else "user"

        # add the contact to contact table
        if receiver_type == "user":
            Contact.add_user_contact(sender, receiver)
            Contact.add_user_contact(receiver, sender)
        else:
            Contact.add_group_contact(sender, receiver)
            group = Group.objects.get(name=receiver)
            usernames = group.get_usernames()
            for username in usernames:
                Contact.add_group_contact(username, receiver)

        # get message and check if the message is found or not
        messages = None
        if is_group(receiver):
            messages = Message.get_group_messages(receiver)
        else:
            messages = Message.get_user_messages(sender, receiver)

        if len(messages) == 0:
            if receiver_type == "user":
                self.send_data_to_user(
                    receiver,
                    "add_contact",
                    {
                        "contact": {
                            "username": sender,
                            "status": get_user_status(sender),
                            "is_direct_message": True,
                        }
                    },
                )
                self.send_data_to_user(
                    sender,
                    "add_contact",
                    {
                        "contact": {
                            "username": receiver,
                            "status": get_user_status(receiver),
                            "is_direct_message": True,
                        }
                    },
                )
            else:
                self.send_data_to_group(
                    receiver,
                    "add_contact",
                    {
                        "contact": {
                            "username": receiver,
                            "status": get_user_status(receiver),
                            "is_direct_message": False,
                        }
                    },
                )

        # create message element
        Message.add_message(sender, receiver, message, receiver_type == "user")
        if receiver_type == "user":
            data["is_direct_message"] = True
            self.send_message_to_user(sender, data)
            self.send_message_to_user(receiver, data)
        else:
            data["is_direct_message"] = False
            self.send_message_to_group(receiver, data)

    def handle_send_message_to_user(self, event):
        data = event["message"]
        self.send(text_data=json.dumps({"type": "SEND_MESSAGE", "data": data}))

    def send_message_to_user(self, user_channel_name, data):
        try:
            async_to_sync(self.channel_layer.group_send)(
                user_channel_name,
                {
                    "type": "handle_send_message_to_user",
                    "message": data,
                },
            )
        except Exception as e:
            print(e)

    def send_message_to_group(self, groupname, data):
        try:
            group = Group.objects.get(name=groupname)
            usernames = group.get_usernames()
            for username in usernames:
                self.send_message_to_user(username, data)
        except Exception as e:
            print(e)

    def update_status(self, event):
        data = event["data"]
        self.send(text_data=json.dumps({"type": "UPDATE_STATUS", "data": data}))

    def add_contact(self, event):
        data = event["data"]
        self.send(text_data=json.dumps({"type": "ADD_CONTACT", "data": data}))

    def send_data_to_user(self, username, type, data):
        try:
            async_to_sync(self.channel_layer.group_send)(
                username,
                {
                    "type": type,
                    "data": data,
                },
            )
        except Exception as e:
            print(e)

    def send_data_to_group(self, groupname, type, data):
        try:
            group = Group.objects.get(name=groupname)
            usernames = group.get_usernames()
            for username in usernames:
                self.send_data_to_user(username, type, data)
        except Exception as e:
            print(e)
