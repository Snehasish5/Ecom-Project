# Generated by Django 5.0.6 on 2024-05-24 13:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pname', models.CharField(max_length=100)),
                ('pprice', models.CharField(max_length=100)),
                ('sdescrip', models.TextField()),
                ('ldescrip', models.TextField()),
                ('quantity', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('active', models.BooleanField(default=True)),
                ('product_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eapp.categories')),
            ],
        ),
    ]
