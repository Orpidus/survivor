# Generated by Django 2.2.5 on 2019-10-16 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_auto_20191010_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='deadline',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='type',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(default='pending', max_length=16),
        ),
    ]
