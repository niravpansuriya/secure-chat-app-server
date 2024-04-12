from django.db import models
from user.models import User
from group.models import Group


class Contact(models.Model):
    user = models.ForeignKey(
        User, related_name="user_contacts", on_delete=models.CASCADE
    )
    user_contact = models.ForeignKey(
        User,
        related_name="contacted_by",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    group_contact = models.ForeignKey(
        Group,
        related_name="contacted_by_group",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    @classmethod
    def add_user_contact(self, username, contact_username):
        user = User.objects.get(username=username)
        user_contact = User.objects.get(username=contact_username)
        Contact.objects.get_or_create(user=user, user_contact=user_contact)

    @classmethod
    def add_group_contact(self, username, group_name):
        user = User.objects.get(username=username)
        group_contact = Group.objects.get(name=group_name)
        Contact.objects.get_or_create(user=user, group_contact=group_contact)

    @classmethod
    def get_contacts(cls, username):
        user = User.objects.get(username=username)
        contacts = Contact.objects.filter(user=user)
        return contacts

    class Meta:
        # unique_together = ("user", "contact")
        unique_together = (("user", "user_contact"), ("user", "group_contact"))
        app_label = "chat_app"


class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    receiver_user = models.ForeignKey(
        User,
        related_name="receiver_user",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    receiver_group = models.ForeignKey(
        Group,
        related_name="receiver_group",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    message = models.TextField()
    is_direct_message = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "chat_app"
        ordering = ["timestamp"]

    @classmethod
    def add_message(cls, sender, receiver, message, is_direct_message=True):
        sender = User.objects.get(username=sender)
        receiver_user = (
            None if is_direct_message == False else User.objects.get(username=receiver)
        )
        receiver_group = (
            None if is_direct_message == True else Group.objects.get(name=receiver)
        )
        return cls.objects.create(
            sender=sender,
            receiver_user=receiver_user,
            receiver_group=receiver_group,
            message=message,
            is_direct_message=is_direct_message,
        )

    @classmethod
    def get_user_messages(cls, party1, party2):
        # Get the users involved in the conversation
        user1 = User.objects.get(username=party1)
        user2 = User.objects.get(username=party2)

        # Query messages between the two parties, sorted by timestamp in ascending order
        messages = cls.objects.filter(
            (models.Q(sender=user1) & models.Q(receiver_user=user2))
            | (models.Q(sender=user2) & models.Q(receiver_user=user1))
        ).order_by("timestamp")

        return messages

    @classmethod
    def get_group_messages(cls, group_name):
        group = Group.objects.get(name=group_name)
        messages = cls.objects.filter(receiver_group=group).order_by("timestamp")
        return messages
