# Generated by Django 4.0.4 on 2022-04-17 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_store', '0004_alter_fooditem_unit_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]