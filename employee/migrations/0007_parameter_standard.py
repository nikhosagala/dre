# Generated by Django 2.0.4 on 2018-04-21 19:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('employee', '0006_auto_20180422_0005'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameter',
            name='standard',
            field=models.IntegerField(default=0),
        ),
    ]
