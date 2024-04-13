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

    # Method to add a user contact
    @classmethod
    def add_user_contact(cls, username, contact_username):
        user = User.objects.get(username=username)
        user_contact = User.objects.get(username=contact_username)
        Contact.objects.get_or_create(user=user, user_contact=user_contact)

    # Method to add a group contact
    @classmethod
    def add_group_contact(cls, username, group_name):
        user = User.objects.get(username=username)
        group_contact = Group.objects.get(name=group_name)
        Contact.objects.get_or_create(user=user, group_contact=group_contact)

    # Method to get contacts for a user
    @classmethod
    def get_contacts(cls, username):
        user = User.objects.get(username=username)
        contacts = Contact.objects.filter(user=user)
        return contacts

    class Meta:
        # Define unique constraints for the Contact model
        unique_together = (("user", "user_contact"), ("user", "group_contact"))
        app_label = "chat_app"


# Define the Message model
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

    # Method to add a message
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

    # Method to get messages between two users
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

    # Method to get messages for a group
    @classmethod
    def get_group_messages(cls, group_name):
        group = Group.objects.get(name=group_name)
        messages = cls.objects.filter(receiver_group=group).order_by("timestamp")
        return messages
