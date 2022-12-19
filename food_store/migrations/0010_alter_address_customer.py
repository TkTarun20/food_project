# Generated by Django 4.0.4 on 2022-06-10 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food_store', '0009_alter_orderitem_unit_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='food_store.customer'),
        ),
    ]