# Generated by Django 2.1.1 on 2018-11-30 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deliver_Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivered_date_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Dispatch_Queue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Dispatch_Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dispatch_date_time', models.DateTimeField()),
                ('dispatch_weight', models.DecimalField(decimal_places=1, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Distance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Forget_password',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=50)),
                ('unitWeight', models.DecimalField(decimal_places=3, max_digits=6)),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=50)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=11)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=11)),
                ('altitude', models.IntegerField()),
                ('Distance', models.ManyToManyField(through='aspsite.Distance', to='aspsite.Location')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=30)),
                ('priority', models.IntegerField()),
                ('dispatchedTime', models.DateTimeField(null=True)),
                ('deliveredTime', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order_Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspsite.Item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspsite.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Pack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itinerary', models.ManyToManyField(to='aspsite.Distance')),
                ('order', models.ManyToManyField(to='aspsite.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Packing_Queue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspsite.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Shipping_Lable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contents', models.CharField(max_length=100)),
                ('final_destination', models.CharField(max_length=20)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspsite.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=6)),
                ('email', models.EmailField(max_length=254)),
                ('userType', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('userType', models.CharField(max_length=20)),
                ('clinic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='aspsite.Location')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(through='aspsite.Order_Item', to='aspsite.Item'),
        ),
        migrations.AddField(
            model_name='order',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspsite.Location'),
        ),
        migrations.AddField(
            model_name='forget_password',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspsite.User'),
        ),
        migrations.AddField(
            model_name='distance',
            name='location1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location1', to='aspsite.Location'),
        ),
        migrations.AddField(
            model_name='distance',
            name='location2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location2', to='aspsite.Location'),
        ),
        migrations.AddField(
            model_name='dispatch_record',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspsite.Order'),
        ),
        migrations.AddField(
            model_name='dispatch_queue',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspsite.Order'),
        ),
        migrations.AddField(
            model_name='deliver_record',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspsite.Order'),
        ),
    ]
