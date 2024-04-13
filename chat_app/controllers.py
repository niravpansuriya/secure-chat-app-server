# Import necessary modules
from user.models import User
from .serializers import ContactSerializer
from .models import Contact
from group.models import Group
from user.models import User
from .serializers import ContactSerializer
from .models import Contact
from group.models import Group


# Define a function to get the status of a user
def get_user_status(username):
    # Check if the username corresponds to a group
    if is_group(username):
        return "online"
    # Get the user object based on the username
    user = User.objects.get(username=username)
    # Determine the status based on the number of sockets the user has
    status = "online" if user.num_sockets > 0 else "offline"
    return status


# Define a function to get the contacts of a user
def get_user_contacts(username):
    # Get the contacts of the user using the Contact model and serialize them
    contacts = ContactSerializer(Contact.get_contacts(username), many=True).data
    # Iterate over each contact and create a dictionary with the required information
    contacts = [
        {
            "username": contact["contact"],
            "status": get_user_status(contact["contact"]),
            "is_direct_message": not is_group(contact["contact"]),
        }
        for contact in contacts
    ]
    return contacts


# Define a function to check if a name corresponds to a group
def is_group(name):
    try:
        # Try to get a group object based on the name
        Group.objects.get(name=name)
        return True
    except:
        return False
