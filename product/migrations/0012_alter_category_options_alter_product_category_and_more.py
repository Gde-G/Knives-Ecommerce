# Generated by Django 4.2.2 on 2023-07-30 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_alter_cart_options_message_have_answered_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'permissions': [('staff_add_category', 'OLP staff add categoty'), ('staff_view_category', 'OLP staff view category'), ('staff_update_category', 'OLP staff update category'), ('staff_delete_category', 'OLP staff delete category')], 'verbose_name_plural': 'Categorias'},
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.category', verbose_name='Categoria'),
        ),
        migrations.AlterField(
            model_name='product',
            name='img_primary',
            field=models.ImageField(upload_to='images/product', verbose_name='Imagen principal'),
        ),
    ]
