# Generated by Django 2.1.1 on 2018-12-01 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aspsite', '0012_auto_20181201_1325'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itinerary', models.ManyToManyField(to='aspsite.Distance')),
                ('order', models.ManyToManyField(to='aspsite.Order')),
            ],
        ),
    ]