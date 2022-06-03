# Generated by Django 3.2.8 on 2022-05-31 14:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tontine', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sanction',
            name='valeur_sanction_presence',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sanction',
            name='valeur_sanction_tontine',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='exercicetontine',
            name='franchise',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 31, 14, 53, 4, 752933, tzinfo=utc)),
        ),
    ]
