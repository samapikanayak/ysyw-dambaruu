# Generated by Django 3.1 on 2022-04-29 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='standard',
            name='image',
            field=models.FileField(null=True, upload_to='image/courses_standard'),
        ),
    ]
