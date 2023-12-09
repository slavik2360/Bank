# Generated by Django 4.2.6 on 2023-12-09 06:15

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, null=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('number', models.CharField(max_length=16, unique=True, validators=[django.core.validators.MinLengthValidator(16)], verbose_name='номер карты')),
                ('cvv', models.CharField(max_length=3, validators=[django.core.validators.MinLengthValidator(3)], verbose_name='cvv')),
                ('date_expiration', models.DateField(default=datetime.datetime(2024, 12, 8, 12, 15, 25, 392064), verbose_name='дата истечения')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Карта',
                'verbose_name_plural': 'Карты',
                'ordering': ('client__user__id', 'datetime_created'),
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, null=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='сумма перевода')),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='transactions_received', to='bank.card', verbose_name='получатель')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='transactions_sended', to='bank.card', verbose_name='отправитель')),
            ],
            options={
                'verbose_name': 'Транзакция',
                'verbose_name_plural': 'Транзакции',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, null=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('account_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(0, message='Баланс не может быть ниже нуля.')])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
                'ordering': ('datetime_created',),
            },
        ),
        migrations.AddField(
            model_name='card',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cards', to='bank.client', verbose_name='владелец'),
        ),
    ]
