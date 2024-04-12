from django.db import models
from user.models import User


# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    @classmethod
    def create_group(self, name, contacts):
        group = Group.objects.create(name=name)
        for contact in contacts:
            contact = User.objects.get(username=contact)
            group.add_user(contact)
        return group


    def add_user(self, user):
        """
        Adds a user to the group.
        """
        self.users.add(user)

    def get_users(self):
        """
        Returns all users belonging to the group.
        """
        return self.users.all()
    
    def get_usernames(self):
        """
        Returns all usernames belonging to the group.
        """
        return [user.username for user in self.users.all()]

    class Meta:
        app_label = "group"
