# Generated by Django 4.2.2 on 2023-07-18 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0025_alter_discountcode_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='total_paid',
            new_name='total_to_pay',
        ),
    ]
