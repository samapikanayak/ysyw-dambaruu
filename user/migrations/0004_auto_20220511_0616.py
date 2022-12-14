# Generated by Django 3.1 on 2022-05-11 06:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20220511_0549'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileAvatar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(upload_to='image/avatar', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg'])])),
                ('name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='person',
            name='profile_picture',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='user.profileavatar'),
        ),
        migrations.DeleteModel(
            name='Profile_Avatar',
        ),
    ]
