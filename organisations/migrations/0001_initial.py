# Generated by Django 4.0.6 on 2022-09-26 14:52

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Organisation',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.CharField(max_length=120)),
                (
                    'employees',
                    models.ManyToManyField(
                        blank=True,
                        related_name='many_users',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'manager',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ('email', models.EmailField(max_length=254)),
                ('is_user_email_exists', models.BooleanField(default=False)),
                ('created_at', models.DateField(auto_now=True)),
                ('state', models.CharField(default='c', max_length=15)),
                (
                    'organisation',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='organisations.organisation',
                    ),
                ),
            ],
        ),
    ]
