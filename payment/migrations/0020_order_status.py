# Generated by Django 4.2.2 on 2023-07-14 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0019_order_shipping_arrives'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('incomplete', 'incomplete'), ('expired', 'expired'), ('approved', 'approved'), ('pending', 'pending'), ('denied', 'denied')], default='incomplete', max_length=12),
        ),
    ]
