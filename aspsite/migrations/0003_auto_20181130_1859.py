# Generated by Django 2.1.1 on 2018-11-30 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aspsite', '0002_auto_20181130_1857'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='shipping_weight',
            new_name='unitWeight',
        ),
        migrations.AddField(
            model_name='item',
            name='name',
            field=models.CharField(default='place_holder', max_length=30),
            preserve_default=False,
        ),
    ]
