# Generated by Django 5.0.3 on 2024-04-11 02:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_initial'),
        ('chat_app', '0005_alter_contact_contact_alter_contact_user_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
