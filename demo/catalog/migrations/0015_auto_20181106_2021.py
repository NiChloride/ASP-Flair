# Generated by Django 2.1.3 on 2018-11-06 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0014_distancebetween2clinics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='distancebetween2clinics',
            name='distance',
            field=models.FloatField(help_text='distance in km'),
        ),
    ]
