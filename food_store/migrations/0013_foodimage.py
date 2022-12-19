# Generated by Django 4.0.6 on 2022-07-09 13:17

from django.db import migrations, models
import django.db.models.deletion
import food_store.validators


class Migration(migrations.Migration):

    dependencies = [
        ('food_store', '0012_remove_customer_first_name_remove_customer_last_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='food_store/images', validators=[food_store.validators.validate_file_size])),
                ('food_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='food_store.fooditem')),
            ],
        ),
    ]