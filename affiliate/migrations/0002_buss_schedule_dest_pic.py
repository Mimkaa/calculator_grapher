# Generated by Django 3.1.7 on 2021-09-22 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affiliate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='buss_schedule',
            name='dest_pic',
            field=models.ImageField(blank=True, null=True, upload_to='images/destinations'),
        ),
    ]
