# Generated by Django 4.2.2 on 2023-07-28 15:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0009_category_add_by_handle_add_by'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartitems',
            options={'verbose_name_plural': 'Producto en el carrito'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categorias'},
        ),
        migrations.AlterModelOptions(
            name='handle',
            options={'verbose_name_plural': 'Empuñaduras'},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-created_at'], 'verbose_name_plural': 'Comentarios'},
        ),
        migrations.AlterModelOptions(
            name='prod_secimg',
            options={'verbose_name_plural': 'Imagenes Secundarias de Productos'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-updated_at'], 'verbose_name_plural': 'Productos'},
        ),
        migrations.AlterField(
            model_name='category',
            name='add_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Creado por'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=70, unique=True, verbose_name='Categoria'),
        ),
        migrations.AlterField(
            model_name='handle',
            name='add_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Agregado por'),
        ),
        migrations.AlterField(
            model_name='handle',
            name='material',
            field=models.CharField(max_length=100, unique=True, verbose_name='Material'),
        ),
        migrations.AlterField(
            model_name='message',
            name='answer',
            field=models.TextField(max_length=512, null=True, verbose_name='Respuesta'),
        ),
        migrations.AlterField(
            model_name='message',
            name='body',
            field=models.TextField(max_length=512, verbose_name='Comentario'),
        ),
        migrations.AlterField(
            model_name='message',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='product.product', verbose_name='Producto correspondiente'),
        ),
        migrations.AlterField(
            model_name='message',
            name='staff_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='awnser_staff_user', to=settings.AUTH_USER_MODEL, verbose_name='Staff que respondio'),
        ),
        migrations.AlterField(
            model_name='message',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Creado por'),
        ),
        migrations.AlterField(
            model_name='product',
            name='add_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Creado por'),
        ),
        migrations.AlterField(
            model_name='product',
            name='blade_material',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Material de la hoja'),
        ),
        migrations.AlterField(
            model_name='product',
            name='blade_size',
            field=models.CharField(default='__ x __ x __ mm', max_length=50, verbose_name='Tamaño de la hoja'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.category', verbose_name='Caregoria'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=400, verbose_name='Descrispción'),
        ),
        migrations.AlterField(
            model_name='product',
            name='handle',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.handle', verbose_name='Empuñadura'),
        ),
        migrations.AlterField(
            model_name='product',
            name='handle_size',
            field=models.CharField(default='__ x __ x __ mm', max_length=50, verbose_name='Tamaño de la empuñadura'),
        ),
        migrations.AlterField(
            model_name='product',
            name='img_primary',
            field=models.ImageField(upload_to='images/product', verbose_name='Imagen princial'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Producto'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Precio'),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='Cantidad'),
        ),
    ]
