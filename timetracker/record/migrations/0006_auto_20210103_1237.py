# Generated by Django 3.1.4 on 2021-01-03 09:07

from django.db import migrations, models
import record.models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0005_auto_20210103_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='avatar',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=record.models.nameFile),
        ),
    ]
