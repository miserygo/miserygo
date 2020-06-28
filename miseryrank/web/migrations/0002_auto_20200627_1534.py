# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2020-06-27 07:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.IntegerField(max_length=10000, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name='Hot',
            fields=[
                ('id', models.IntegerField(max_length=10000, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=10000)),
                ('content', models.CharField(blank=True, max_length=10000, null=True)),
                ('url', models.CharField(max_length=10000)),
                ('block_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hot', to='web.Block')),
            ],
        ),
        migrations.AddField(
            model_name='block',
            name='hots',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='web.Hot'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='collect',
            field=models.ManyToManyField(to='web.Hot'),
        ),
    ]