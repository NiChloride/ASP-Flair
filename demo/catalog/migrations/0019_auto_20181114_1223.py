# Generated by Django 2.1.3 on 2018-11-14 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_auto_20181114_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='priority',
            field=models.CharField(choices=[('c', 'Low'), ('b', 'Medium'), ('a', 'High')], help_text='Enter priority.', max_length=1),
        ),
    ]
