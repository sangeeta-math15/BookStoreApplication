# Generated by Django 4.1.2 on 2022-10-12 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='user',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='cartitem',
            old_name='user',
            new_name='user_id',
        ),
        migrations.AlterField(
            model_name='cart',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]