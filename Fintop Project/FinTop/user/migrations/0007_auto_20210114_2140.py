# Generated by Django 3.1.4 on 2021-01-14 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_additional_assets_select'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='additional_assets',
            options={'verbose_name': 'Additional_assets', 'verbose_name_plural': 'Additional_assets'},
        ),
        migrations.RemoveField(
            model_name='additional_assets',
            name='select',
        ),
    ]
