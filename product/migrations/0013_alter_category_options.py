# Generated by Django 4.2.2 on 2023-07-30 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_alter_category_options_alter_product_category_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'permissions': [('staff_add_category', 'OLP staff add categoty'), ('staff_view_category', 'OLP staff view category'), ('staff_change_category', 'OLP staff change category'), ('staff_delete_category', 'OLP staff delete category')], 'verbose_name_plural': 'Categorias'},
        ),
    ]
