# Generated by Django 2.2.5 on 2019-10-10 10:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('task', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='advocate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.Advocate'),
        ),
        migrations.AddField(
            model_name='task',
            name='survivor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Survivor'),
        ),
    ]
