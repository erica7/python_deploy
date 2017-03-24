# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-24 14:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_and_reg', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote', models.TextField()),
                ('author', models.CharField(max_length=90)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('favorites', models.ManyToManyField(related_name='favorite_quotes', to='login_and_reg.User')),
                ('user_contributor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_contributions', to='login_and_reg.User')),
            ],
        ),
    ]