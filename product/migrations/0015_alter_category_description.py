# Generated by Django 4.2.2 on 2023-08-03 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_alter_category_options_alter_handle_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, max_length=400, null=True, verbose_name='Descripción'),
        ),
    ]
