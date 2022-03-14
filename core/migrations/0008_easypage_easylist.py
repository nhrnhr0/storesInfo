# Generated by Django 4.0.3 on 2022-03-14 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_place_isbusiness'),
    ]

    operations = [
        migrations.CreateModel(
            name='EasyPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='EasyList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=200)),
                ('isLoaded', models.BooleanField(default=False)),
                ('pages', models.ManyToManyField(to='core.easypage')),
            ],
        ),
    ]
