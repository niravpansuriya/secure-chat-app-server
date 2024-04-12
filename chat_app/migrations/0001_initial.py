# Generated by Django 5.0.3 on 2024-04-09 13:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0002_user_sockets'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacted_by', to='authentication.user')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_contacts', to='authentication.user')),
            ],
            options={
                'unique_together': {('user', 'contact')},
            },
        ),
    ]
