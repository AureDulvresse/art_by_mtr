# Generated by Django 5.0.6 on 2024-06-22 21:54

from django.db import migrations


def change_storage_engine_to_innodb(apps, schema_editor):
    tables = [
        'store_category',
        'store_medium',
        'store_artwork',
        'store_order',
        'store_checkout',
        'store_cart',
    ]
    for table in tables:
        schema_editor.execute(f'ALTER TABLE {table} ENGINE = InnoDB;')

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),  # Remplacez par la dernière migration générée
    ]

    operations = [
        migrations.RunPython(change_storage_engine_to_innodb),
    ]