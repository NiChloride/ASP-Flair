# Generated by Django 2.1.3 on 2018-11-06 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_auto_20181106_1606'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clinic',
            old_name='alt',
            new_name='altitude',
        ),
        migrations.RenameField(
            model_name='clinic',
            old_name='lat',
            new_name='latitude',
        ),
        migrations.RenameField(
            model_name='clinic',
            old_name='long',
            new_name='longitude',
        ),
        migrations.AlterField(
            model_name='ordersupplymatching',
            name='numberofsupply',
            field=models.IntegerField(default=0, help_text='Number of supply needed'),
        ),
    ]
