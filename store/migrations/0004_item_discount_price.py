# Generated by Django 4.0.6 on 2022-09-04 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_item_slug_alter_item_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='discount_price',
            field=models.DecimalField(decimal_places=0, default=150, max_digits=10),
        ),
    ]
