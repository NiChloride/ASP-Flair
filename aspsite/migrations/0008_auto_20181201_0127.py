# Generated by Django 2.1.1 on 2018-11-30 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aspsite', '0007_auto_20181201_0125'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='category',
        ),
        migrations.DeleteModel(
            name='ItemCategory',
        ),
    ]
