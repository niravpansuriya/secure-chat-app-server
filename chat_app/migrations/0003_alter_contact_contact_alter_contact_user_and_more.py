# Generated by Django 5.0.3 on 2024-04-11 02:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_app', '0002_message'),
        ('user', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacted_by', to='user.user'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_contacts', to='user.user'),
        ),
        migrations.AlterField(
            model_name='message',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='user.user'),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='user.user'),
        ),
    ]
