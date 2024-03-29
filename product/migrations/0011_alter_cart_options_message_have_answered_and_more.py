# Generated by Django 4.2.2 on 2023-07-30 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_alter_cartitems_options_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name_plural': 'Carrito'},
        ),
        migrations.AddField(
            model_name='message',
            name='have_answered',
            field=models.BooleanField(default=False, verbose_name='Fue respondido?'),
        ),
        migrations.AlterField(
            model_name='prod_secimg',
            name='img_sec_4',
            field=models.ImageField(null=True, upload_to='images/prod-sec'),
        ),
        migrations.AlterField(
            model_name='prod_secimg',
            name='img_sec_5',
            field=models.ImageField(null=True, upload_to='images/prod-sec'),
        ),
    ]
