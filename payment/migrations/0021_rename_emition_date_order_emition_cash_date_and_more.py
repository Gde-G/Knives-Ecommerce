# Generated by Django 4.2.2 on 2023-07-14 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0020_order_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='emition_date',
            new_name='emition_cash_date',
        ),
        migrations.AddField(
            model_name='order',
            name='expiration_cash_date',
            field=models.DateTimeField(null=True),
        ),
    ]
