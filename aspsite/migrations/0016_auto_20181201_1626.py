# Generated by Django 2.1.1 on 2018-12-01 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aspsite', '0015_auto_20181201_1415'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Drone',
            new_name='Pack',
        ),
        migrations.AlterField(
            model_name='token',
            name='token',
            field=models.CharField(max_length=10),
        ),
    ]