# Generated by Django 3.1.5 on 2021-02-09 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_auto_20210207_2215'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='/home/ubuntu/Fintop/Fintop/Fintop Project/FinTop/agreement/'),
        ),
    ]
