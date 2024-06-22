# Generated by Django 5.0.6 on 2024-06-22 22:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed'), ('Refunded', 'Refunded')], max_length=15)),
                ('checkout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.checkout')),
            ],
            options={
                'db_table': 'store_payment',
                'ordering': ['-created_at'],
            },
        ),
    ]