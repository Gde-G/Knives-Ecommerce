# Generated by Django 4.2.2 on 2023-07-13 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0017_alter_order_paymethod_cash_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paymethod_wallet_type',
            field=models.CharField(blank=True, choices=[('paypal', 'paypal'), ('mercadopago', 'mercadopago'), ('brubank', 'brubank')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='paymethod_cash_type',
            field=models.CharField(blank=True, choices=[('pagofacil', 'pagofacil'), ('rapipago', 'rapipago'), ('western union', 'western union')], max_length=17, null=True),
        ),
    ]
