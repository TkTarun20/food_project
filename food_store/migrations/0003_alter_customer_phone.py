# Generated by Django 4.0.4 on 2022-04-17 15:18

import django.core.validators
from django.db import migrations, models
import food_store.validators


class Migration(migrations.Migration):

    dependencies = [
        ('food_store', '0002_alter_address_pincode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(10), food_store.validators.validate_integers]),
        ),
    ]