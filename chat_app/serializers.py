# serializers.py
from rest_framework import serializers
from .models import Message, Contact
from user.models import User
from group.models import Group


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(source="sender.username")
    receiver = serializers.StringRelatedField(source="receiver.username")

    class Meta:
        model = Message
        fields = ["sender", "receiver", "message", "is_direct_message", "timestamp"]


class MixedContactField(serializers.SerializerMethodField):
    def to_representation(self, value):
        if value.user_contact:
            return value.user_contact.username
        elif value.group_contact.name:
            return value.group_contact.name
        return None

    def get_queryset(self):
        return None

    def to_internal_value(self, data):
        return None


class ContactSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(source="user.username")
    # contact = serializers.StringRelatedField(source="contact.username")
    contact = MixedContactField(allow_null=True)

    class Meta:
        model = Contact
        fields = ["user", "contact"]
