# Generated by Django 4.2.2 on 2023-07-17 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0024_alter_order_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discountcode',
            name='code',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
