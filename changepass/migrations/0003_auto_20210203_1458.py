# Generated by Django 3.1.1 on 2021-02-03 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0053_auto_20210130_1510'),
        ('changepass', '0002_auto_20210203_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpcode',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.consumer'),
        ),
    ]
