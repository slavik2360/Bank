# Generated by Django 4.2.6 on 2023-11-07 14:27

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('datetime_created', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, null=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('first_name', models.CharField(max_length=40, verbose_name='имя')),
                ('last_name', models.CharField(max_length=40, verbose_name='фамилия')),
                ('email', models.CharField(max_length=60, unique=True, verbose_name='почта/логин')),
                ('password', models.CharField(max_length=128, validators=[django.core.validators.MinLengthValidator(7)], verbose_name='пароль11')),
                ('password2', models.CharField(max_length=128, validators=[django.core.validators.MinLengthValidator(7)], verbose_name='пароль2')),
                ('gender', models.SmallIntegerField(choices=[('MALE', 'Мужчина'), ('FEMALE', 'Женщина')], null=True, verbose_name='gender')),
                ('is_active', models.BooleanField(default=False, verbose_name='активный?')),
                ('is_staff', models.BooleanField(default=False, verbose_name='это персонал')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Суперпользователь')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'ordering': ('datetime_created',),
            },
        ),
    ]
