# Generated by Django 4.0.6 on 2022-09-04 20:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_orderitem_ordered_orderitem_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='ordered',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='user',
        ),
    ]
