# Generated by Django 3.1.1 on 2021-02-03 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('changepass', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpcode',
            name='create_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]