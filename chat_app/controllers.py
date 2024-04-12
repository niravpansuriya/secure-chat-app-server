from user.models import User
from .serializers import ContactSerializer
from .models import Contact
from group.models import Group


def get_user_status(username):
    if is_group(username):
        return "online"

    user = User.objects.get(username=username)
    status = "online" if user.num_sockets > 0 else "offline"
    return status


def get_user_contacts(username):
    contacts = ContactSerializer(Contact.get_contacts(username), many=True).data
    contacts = [
        {
            "username": contact["contact"],
            "status": get_user_status(contact["contact"]),
            "is_direct_message": not is_group(contact["contact"]),
        }
        for contact in contacts
    ]
    # contacts = [contact["contact"] for contact in contacts]
    return contacts


def is_group(name):
    try:
        Group.objects.get(name=name)
        return True
    except:
        return False
