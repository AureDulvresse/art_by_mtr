# Generated by Django 5.0.6 on 2024-07-28 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='currency',
            field=models.CharField(choices=[('EUR', 'EUR'), ('USD', 'USD')], default='EUR', max_length=3),
        ),
    ]
