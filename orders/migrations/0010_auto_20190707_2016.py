# Generated by Django 2.2.3 on 2019-07-07 20:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_remove_cart_pizza'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='pizza',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.Pizza'),
        ),
    ]
