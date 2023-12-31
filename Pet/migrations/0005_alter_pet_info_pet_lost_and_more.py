# Generated by Django 4.2.4 on 2023-08-08 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pet', '0004_remove_pet_info_id_alter_pet_info_register_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet_info',
            name='pet_lost',
            field=models.CharField(choices=[('Y', 'YES'), ('N', 'NO')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='pet_info',
            name='register_number',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
