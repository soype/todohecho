# Generated by Django 3.2.2 on 2021-06-21 17:54

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='Email')),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='Usuario')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Fecha en que se unió')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='Última sesión')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('profile_image', models.ImageField(blank=True, default=accounts.models.get_default_profile_image, max_length=255, null=True, upload_to=accounts.models.get_profile_image_filepath)),
                ('first_name', models.CharField(max_length=60, verbose_name='Nombre')),
                ('last_name', models.CharField(max_length=60, verbose_name='Apellido')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
