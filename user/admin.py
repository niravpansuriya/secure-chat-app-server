from django.contrib import admin
from .models import User
from chat_app.models import Contact, Message
from group.models import Group

# Register your models here.
admin.site.register(User)
admin.site.register(Contact)
admin.site.register(Message)
admin.site.register(Group)
